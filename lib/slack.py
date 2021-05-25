import	ast
import 	glob
import	importlib
import	inspect
import	logging
import	os
import	re
from slack_bolt import BoltRequest

# from http.server import  HTTPServer
# from pyngrok import ngrok
# from threading import Thread

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
# from lib.server import WebhookServerHandler
class app:
	app_dir = os.getcwd()
	plugins_dir = app_dir + os.sep +  'plugins'
	app_token:str = os.environ.get("JIBOT_SLACK_APP_TOKEN", None)
	bot_token:str = os.environ.get("JIBOT_SLACK_BOT_TOKEN", None)
	bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
	client_id:str = os.environ.get("JIBOT_SLACK_CLIENT_ID", None)
	client_secret:str = os.environ.get("JIBOT_SLACK_CLIENT_SECRET", None)
	signing_secret:str = os.environ.get("JIBOT_SLACK_SIGNING_SECRET", None)
	user_token:str = os.environ.get("JIBOT_SLACK_USER_TOKEN", None)
	verification_token:str = os.environ.get("JIBOT_SLACK_VERIFICATION_TOKEN", None)
	port = int(os.environ.get("JIBOT_PORT", 3000))
	webhook_proxy_port = int(os.environ.get("JIBOT_WEBSOCKET_PORT", port))
	webhook_proxy_server = None
	webhook_url:str = os.environ.get("JIBOT_SLACK_WEBHOOK_URL", None)
	webhook_client:WebhookClient = WebhookClient(webhook_url) if webhook_url is not None else None
	ngrok_token:str = os.environ.get("JIBOT_NGROK_AUTH_TOKEN", None)
	ngrok_hostname:str = os.environ.get("JIBOT_NGROK_HOSTNAME", None)
	has_ngrok:bool = True if ngrok_token is not None else False
	do_socket_mode:bool = ast.literal_eval(os.environ.get("JIBOT_DO_SOCKET_MODE", 'True'))
	api_connected:bool = False
	bot_user = None
	channels = None
	users = None
	# folder_plugin_types:set = {
	# 	'command': {},
	# 	'event': {}
	# }
	plugin_mapper:dict = {
		'command': {},
		'event': {}
	}
	app_welcome_message:list = []
	bot_welcome_message:list = []
	logging = logging

	def __init__(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		self.bolt = App(
			signing_secret = self.signing_secret,
			token = self.bot_token,
		)
		logging.Logger.slack = self.log_to_slack
		self.logging = logging.getLogger(self.bolt.name.upper())
		self.test_slack_client_connection()
		self.who_is_bot()
		self.get_slack_info()
		self.bot_says_hi()
		self.load_plugins()
		self.bolt.use(self.global_listener)
		try:
			self.start()
		except KeyboardInterrupt:
			self.logging.slack("*Shutting down...*")
			self.close()

	def log_to_slack(self, message, *args, **kwargs):
		self.logging.info(message)
		if self.webhook_client is not None:
			self.webhook_client.send(text=message)

	def slack_api_error(self, error: SlackApiError):
		error_name = error.response['error']
		assert(error_name)
		if error_name == 'missing_scope':
			missing_scope = error.response['needed']
			message = f"The bot is missing proper oauth scope!({missing_scope}). Scopes are added to your bot at https://api.slack.com/apps."
			self.logging.error(message)
			self.logging.slack(message)

		self.logging.error(error)

	def load_plugins(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		plugin_files = glob.glob(self.plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
		path_regex = re.compile("^plugins\/(\w+)\/(.+)\.py$")
		log_message:list = []
		self.app_welcome_message.append("Loading slack plugins... ")
		for plugin_path in plugin_files:
			relative_path = os.path.relpath(plugin_path, os.getcwd())
			matches = path_regex.match(relative_path)
			if matches is not None:
				plugin = {
					"path": plugin_path,
					"import_path": matches.group(0).replace(".py", "").replace("/","."),
					"type": matches.group(1),
					"name": matches.group(2),
				}
				plugin['lib'] = importlib.import_module(plugin.get('import_path'))
				keyword = plugin.get('name')
				try:
					keyword = plugin.get('lib').keyword
				except AttributeError as e:
					assert(e)
				plugin['keyword'] = keyword
				try:
					plugin['callback_function'] = plugin.get('lib').callback_function
				except:
					self.logging.debug("Skipping plugin with no callback...")
				if plugin.get('callback_function') is not None:
					plugin_type = plugin.get('type')
					handler_function:callable = getattr(self.bolt, plugin_type)
					if plugin_type in self.plugin_mapper.keys():
						arg_regex = re.compile("((?P<event_name>\w+)\/)?(?P<arg>\w+)")
						matches = re.finditer(arg_regex, plugin.get('keyword'))
						if matches is not None:
							for match in matches:
								event_name = match.group('event_name')
								keyword = match.group('arg')
								if event_name is not None:
									print(f"!{event_name}:{keyword}")
								else:
									print(f"{plugin_type}!{keyword}")
									self.plugin_mapper[plugin_type][keyword] = plugin.get('callback_function')
					else:
						handler_function(plugin.get('keyword'))(plugin.get('callback_function'))

					# if plugin_type == 'command':
					# 	self.plugin_mapper[plugin_type][keyword] = plugin.get('callback_function')
					# else:
					# 	print(plugin)
					# 	print(plugin)
					# 	print(plugin)
					# 	print(plugin)
					# if plugin_type == 'event':
					# 	event_regex = re.compile("((?P<event_name>\w+)\/)?(?P<name>\w+)")
					# 	matches = re.finditer(event_regex, plugin.get('keyword'))
					# 	if matches is not None:
					# 		for match in matches:
					# 			event_name = match.group('event_name')
					# 			name = match.group('name')
					# 			# print(event_name)
					# 			# print(name)
					# 			# print(plugin)
					# 	else:
					# 		print("ASKDJALKSJDLKASJDLKAJSLDKJASLKDJSA")
					# 		print(plugin)
					# else:


		if self.bot_slash_command is not None:
			log_message.append(f"Bot has a slash command (/{self.bot_slash_command}), setup command listener...")
			self.bolt.command(f"/{self.bot_slash_command}")(self.command_listener)


		self.event_listener = self.command_listener
		self.bolt.event("app_mention")(self.event_listener)
		self.app_welcome_message.append("\r".join(log_message))

	def start(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		self.app_welcome_message.append("*Starting bot listeners...*")
		self.logging.slack("\r".join(self.app_welcome_message))
		# if (self.has_ngrok is True):
		# 	self.app_welcome_message.append("Detected ngrok, starting webhook tunnel...")
		# 	self.webhook_proxy_server = Thread(target=self.start_webhook_http_server)
		# 	self.webhook_proxy_server.start()
		# 	ngrok_tunnel = ngrok.connect(
		# 		self.webhook_proxy_port,
		# 		"http",
		# 		subdomain=self.ngrok_hostname,
		# 	)
		# 	self.app_welcome_message.append("Webhook proxy url is: " + ngrok_tunnel.public_url)
		if self.do_socket_mode is True:
			self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
			self.app_welcome_message.append("Starting bolt app in Socket mode....")
			self.socket_mode.start()
		else:
			self.bolt.start(port=self.port)

	def close(self):
		self.logging.info(inspect.currentframe().f_code.co_name)
		self.logging.info("*Shutting jibot down...*")
		if self.do_socket_mode is True:
			self.logging.info("Disconnecting socket mode...")
			self.socket_mode.disconnect()
		# if self.has_ngrok is True:
		# 	self.logging.info("Shutting down ngrok and webhook proxy...")
		# 	ngrok.kill()
		# 	self.webhook_proxy_server.

	# def start_webhook_http_server(self):
	# 	self.logging.debug(inspect.currentframe().f_code.co_name)
	# 	self.app_welcome_message.append("Setting up a simple http server to act as a webhook proxy...")
	# 	webhook_server_address = ('localhost', self.webhook_proxy_port)
	# 	webhook_server = HTTPServer(webhook_server_address, WebhookServerHandler)
	# 	webhook_server.serve_forever()

	def test_slack_client_connection(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		try:
			self.api_connected = self.bolt.client.api_test().get("ok")
			self.app_welcome_message.append("Slack web client connection established...")
		except SlackApiError as e:
			self.logging.error("Unable to establish a slack web client connection!")
			self.slack_api_error(e)

	def who_is_bot(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		try:
			bot_auth = self.bolt.client.auth_test(token=self.bot_token)
			self.bot_user = self.bolt.client.users_info(user=bot_auth.get("user_id")).get("user")
			self.app_welcome_message.append(f"Starting jibot ({self.bot_user.get('real_name')}).")
			self.logging.debug(self.bot_user)
		except SlackApiError as e:
			self.slack_api_error(e)

	def bot_says_hi(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if self.channels is not None:
			bot_channels:list = []
			for channel in self.channels:
				try:
					channel_members =  self.bolt.client.conversations_members(channel=channel.get('id')).get('members')
					if self.bot_user is not None and self.bot_user.get('id') in channel_members:
						bot_channels.append(channel.get('id'))
						self.logging.slack(f"I am on #{channel.get('name')}. The bot say hello.")
						self.bolt.client.chat_postMessage(
							channel=channel.get('id'),
							text=f"Hello #{channel.get('name')}! I am {self.bot_user.get('real_name')}. I am waking up."
						)
				except SlackApiError as e:
					self.slack_api_error(e)
			if len(bot_channels) == 0:
				self.logging.warning("The bot is NOT on any slack channels. Should we consider having the bot create a channel (if scopes allow)? You can also add bot to a channel via @mention_bot_name")

	def get_slack_info(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if self.bot_user is not None:
			team_id = self.bot_user.get("team_id", None)
			try:
				self.team = self.bolt.client.team_info(team=team_id).get("team")
				self.channels = self.bolt.client.conversations_list().get('channels')
				self.users = self.bolt.client.users_list().get('members')
			except SlackApiError as e:
				self.slack_api_error(e)

	def command_listener(self, ack, client, command, context, event, logger, next, payload, request:BoltRequest, response, respond, say):
		logger.debug(inspect.currentframe().f_code.co_name)
		callback_args = locals()
		event_type:str = None
		text = payload.get('text')
		keyword = text.split()[0] if text is not None else None
		del(callback_args['self'])
		if command is not None: event_type = "command"
		if event is not None: event_type = "event"
		args = list(callback_args.keys())
		for i in args:
			arg = callback_args[i]
			if arg is None:
				del(callback_args[i])

		if keyword is not None:
			if keyword in self.plugin_mapper[event_type].keys():
			 	# SLASH COMMANDS WORK / EVENTS NOT YET
				callback_function = self.plugin_mapper[event_type][keyword]
				callback_function(**callback_args)

	def global_listener(self, logger, next, payload, request, response, respond, say):
		logger.debug(inspect.currentframe().f_code.co_name)
		logger.debug(payload)
		next()
	pass