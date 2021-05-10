import	ast
import 	glob
import	importlib
import	inspect
import	logging
import	os
import	re
from 	logging import Logger
from 	pyngrok import ngrok

from slack_bolt import App
from slack_bolt.error import BoltError
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.authorization import  AuthorizeResult
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient

logging.addLevelName(logging.INFO + 3, 'SLACK')

class app:
	app_token:str = os.environ.get("JIBOT_SLACK_APP_TOKEN", None)
	bot_token:str = os.environ.get("JIBOT_SLACK_BOT_TOKEN", None)
	bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
	client_id:str = os.environ.get("JIBOT_SLACK_CLIENT_ID", None)
	client_secret:str = os.environ.get("JIBOT_SLACK_CLIENT_SECRET", None)
	signing_secret:str = os.environ.get("JIBOT_SLACK_SIGNING_SECRET", None)
	user_token:str = os.environ.get("JIBOT_SLACK_USER_TOKEN", None)
	verification_token:str = os.environ.get("JIBOT_SLACK_VERIFICATION_TOKEN", None)
	port = int(os.environ.get("JIBOT_PORT", 3000))
	webhook_url:str = os.environ.get("JIBOT_SLACK_WEBHOOK_URL", None)
	webhook:WebhookClient = WebhookClient(webhook_url) if webhook_url is not None else None

	ngrok_token:str = os.environ.get("JIBOT_NGROK_AUTH_TOKEN", None)
	ngrok_hostname:str = os.environ.get("JIBOT_NGROK_HOSTNAME", None)
	has_ngrok:bool = True if ngrok_token is not None else False
	do_socket_mode:bool = ast.literal_eval(os.environ.get("JIBOT_DO_SOCKET_MODE", 'True'))

	api_connected:bool = False
	bot_user = None
	channels = None
	users = None
	command_plugins:dict = {}

	app_welcome_message:list = []
	bot_welcome_message:list = []
	logging = logging

	def log_to_slack(self, message, *args, **kwargs):
		self.logging.info(message)
		if self.webhook is not None:
			self.webhook.send(text=message)

	def __init__(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		self.bolt = App(
			raise_error_for_unhandled_request=False,
			signing_secret = self.signing_secret,
			token = self.bot_token,
			verification_token = self.verification_token
		)
		logging.Logger.slack = self.log_to_slack
		self.logging = logging.getLogger(self.bolt.name.upper())
		self.test_slack_client_connection()
		self.get_slack_info()
		self.who_is_bot()
		self.bot_says_hi()
		self.load_plugins()
		# self.bolt.use(self.global_listener)
		try:
			self.app_welcome_message.append("*Starting bot listeners...*")
			self.logging.slack("\r".join(self.app_welcome_message))
			self.start()
		except KeyboardInterrupt:
			self.close()

	def slack_api_error(self, error: SlackApiError):
		error_name = error.response['error']
		assert(error_name)
		if error_name == 'missing_scope':
			message = f"The bot is missing proper oauth scope!({missing_scope}). Scopes are added to your bot at https://api.slack.com/apps."
			missing_scope = error.response['needed']
			this.logging.error(message)
			this.logging.slack(message)
		logging.error(error.response)

	def load_plugins(self):
		self.app_welcome_message.append(f"Loading slack plugins...")
		app_dir = os.getcwd()
		plugins_dir = app_dir + os.sep +  'plugins'
		plugin_files = glob.glob(plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
		path_regex = re.compile("^plugins\/(\w+)\/(.+)\.py$")
		log_message:list = []
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
					log_message.append(f"This plugin has a keyword specified ('{keyword}'), this overrides using the plugin filename as the keyword.")
				except AttributeError as e:
					assert(e)
				plugin['keyword'] = keyword
				plugin['callback_function'] = plugin.get('lib').callback_function
				handler_function:callable = getattr(self.bolt, plugin.get('type'))
				if plugin.get('type') == 'command':
					self.command_plugins[keyword] = plugin.get('callback_function')
				else:
					handler_function(plugin.get('keyword'))(plugin.get('callback_function'))
		if self.bot_slash_command is not None:
			log_message.append(f"Bot has a slash command (/{self.bot_slash_command}), setup command listener...")
			self.bolt.command(f"/{self.bot_slash_command}")(self.command_listener)
		self.app_welcome_message.append("\r\t".join(log_message))

	def start(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if self.do_socket_mode is True:
			self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
			self.app_welcome_message.append("Starting bolt app in Socket mode....")
			self.socket_mode.start()

		else:
			if (self.has_ngrok is True):
				self.app_welcome_message.append("Detected ngrok... starting request url tunnel...")
				request_url_tunnel = ngrok.connect(self.port, "http", subdomain=self.ngrok_hostname)
				ngrok_process = ngrok.get_ngrok_process()
				self.app_welcome_message.append("Request Url is: " + request_url_tunnel.public_url)
			self.bolt.start(port=self.port)

	def close(self):
		self.logging.slack("*Shutting jibot down...*")
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if (self.has_ngrok is True):
			ngrok.kill()

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
			self.app_welcome_message.append(f"Starting jibot. Jibot is named '{self.bot_user.get('real_name')}.'")
			self.logging.slack(self.bot_user)
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
						self.logging.slack(f"I am on #{channel.get('name')}. I should say hello.")
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

	def command_listener(self, ack, client, command, context, logger, next, options, payload, request, response, respond, say):
		callback_args = locals()
		del(callback_args['self'])
		logger.info(inspect.currentframe().f_code.co_name)
		command_text:str = command.get('text', None)
		keyword = command_text.split()[0] if command_text is not None else None
		callback_function = self.command_plugins.get(keyword, None) if keyword is not None else None
		if callback_function is not None:
			callback_function(**callback_args)
			ack()

	def global_listener(self, ack, action, client, command, context, event, logger, message, next, options, payload, request, response, respond, say, shortcut, view):
		logger.info(inspect.currentframe().f_code.co_name)
		logger.debug(payload)
		next()
	pass