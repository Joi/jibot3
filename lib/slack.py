import ast
import glob
import inspect
import logging
import os
import re
from slack_bolt import BoltRequest

# from http.server import  HTTPServer
# from pyngrok import ngrok
# from threading import Thread

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.kwargs_injection import build_required_kwargs
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
from slack_sdk.web import WebClient

from lib.plugin import Plugin
# from lib.server import WebhookServerHandler

whitespace:str = "|".join([' ', '\xa0'])
def get_bot_mention_text(bot_id, text):
	if text is None: return text
	logging.debug(inspect.currentframe().f_code.co_name)
	global whitespace
	space_re = f"({whitespace})+"
	bot_mention_re:str = f"<@(?P<bot_id>{bot_id})>"
	regex:re = re.compile(f"(?P<pretext>.*)(?P<bot_mention>{bot_mention_re}){space_re}(?P<text>.+)")
	matches = re.finditer(regex, text)
	mention_text = []
	if matches is not None:
		for match in matches: mention_text.append(match.group('text'))
	if len(mention_text) == 0: return(text)
	elif len(mention_text) == 1: return(mention_text[0])
	else: return mention_text

class app:
	bolt:App = None
	app_dir:str = os.getcwd()
	plugins_dir:str = app_dir + os.sep +  'plugins'
	app_token:str = os.environ.get("JIBOT_SLACK_APP_TOKEN", None)
	bot_token:str = os.environ.get("JIBOT_SLACK_BOT_TOKEN", None)
	bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
	client_id:str = os.environ.get("JIBOT_SLACK_CLIENT_ID", None)
	client_secret:str = os.environ.get("JIBOT_SLACK_CLIENT_SECRET", None)
	signing_secret:str = os.environ.get("JIBOT_SLACK_SIGNING_SECRET", None)
	user_token:str = os.environ.get("JIBOT_SLACK_USER_TOKEN", None)
	verification_token:str = os.environ.get("JIBOT_SLACK_VERIFICATION_TOKEN", None)
	port = int(os.environ.get("JIBOT_PORT", 3000))
	# webhook_proxy_port = int(os.environ.get("JIBOT_WEBSOCKET_PORT", port))
	# webhook_proxy_server = None
	# webhook_url:str = os.environ.get("JIBOT_SLACK_WEBHOOK_URL", None)
	# webhook_client:WebhookClient = WebhookClient(webhook_url) if webhook_url is not None else None
	# ngrok_token:str = os.environ.get("JIBOT_NGROK_AUTH_TOKEN", None)
	# ngrok_hostname:str = os.environ.get("JIBOT_NGROK_HOSTNAME", None)
	# has_ngrok:bool = True if ngrok_token is not None else False
	do_socket_mode:bool = ast.literal_eval(os.environ.get("JIBOT_DO_SOCKET_MODE", 'True'))
	bot_user = None
	channels = None
	bot_channels:list = []
	users = None
	plugins:list = []
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
		self.bolt.use(self.global_middleware_listener)
		self.load_plugins()
		try:
			self.start()
		except KeyboardInterrupt:
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
		if self.bot_slash_command is not None:
			self.bolt.command(f"/{self.bot_slash_command}")(self.events_with_arguments_listener)
		plugin_files = glob.glob(self.plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
		path_regex = re.compile("^plugins\/(\w+)\/(.+)\.py$")
		for plugin_path in plugin_files:
			relative_path = os.path.relpath(plugin_path, os.getcwd())
			matches = path_regex.match(relative_path)
			if matches is not None:
				file_name = matches.group(2)
				import_path = matches.group(0).replace(".py", "").replace(os.sep, ".")
				plugin_type = matches.group(1)
				plugin = Plugin(file_name, import_path, plugin_type)
				self.plugins.append(plugin)
				bolt_event_handler:callable = getattr(self.bolt, plugin.type)
				if plugin.type == 'command' or plugin.event_name is not None:
					bolt_event_handler(plugin.event_name)(self.events_with_arguments_listener)
				else:
					listener_keyword_or_regex = plugin.keyword
					if plugin.regex is not None:
						listener_keyword_or_regex = plugin.regex
					bolt_event_handler(listener_keyword_or_regex)(plugin.callback)

	def start(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		# if (self.has_ngrok is True):
		# 	self.webhook_proxy_server = Thread(target=self.start_webhook_http_server)
		# 	self.webhook_proxy_server.start()
		# 	ngrok_tunnel = ngrok.connect(
		# 		self.webhook_proxy_port,
		# 		"http",
		# 		subdomain=self.ngrok_hostname,
		# 	)
		if self.do_socket_mode is True:
			self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
			self.socket_mode.start()
		else:
			self.bolt.start(port=self.port)

	def close(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		self.bot_says_bye()
		if self.do_socket_mode is True:
			self.logging.info("Disconnecting socket mode...")
			self.socket_mode.disconnect()
		# if self.has_ngrok is True:
		# 	self.logging.info("Shutting down ngrok and webhook proxy...")
		# 	ngrok.kill()
		# 	self.webhook_proxy_server.

	# def start_webhook_http_server(self):
	# 	self.logging.debug(inspect.currentframe().f_code.co_name)
	# 	webhook_server_address = ('localhost', self.webhook_proxy_port)
	# 	webhook_server = HTTPServer(webhook_server_address, WebhookServerHandler)
	# 	webhook_server.serve_forever()

	def test_slack_client_connection(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		try:
			self.bolt.client.api_test().get("ok")
		except SlackApiError as e:
			self.logging.error("Unable to establish a slack web client connection!")
			self.slack_api_error(e)

	def who_is_bot(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		try:
			bot_auth = self.bolt.client.auth_test(token=self.bot_token)
			self.bot_user = self.bolt.client.users_info(user=bot_auth.get("user_id")).get("user")
			self.logging.debug(self.bot_user)
		except SlackApiError as e:
			self.slack_api_error(e)

	def bot_says_hi(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if self.channels is not None:
			for channel in self.channels:
				try:
					channel_members =  self.bolt.client.conversations_members(channel=channel.get('id')).get('members')
					if self.bot_user is not None and self.bot_user.get('id') in channel_members:
						self.bot_channels.append(channel)
						self.bolt.client.chat_postMessage(
							channel=channel.get('id'),
							text=f"Hello #{channel.get('name')}! I am waking up."
						)
				except SlackApiError as e:
					self.slack_api_error(e)

	def bot_says_bye(self):
		self.logging.debug(inspect.currentframe().f_code.co_name)
		if self.bot_channels is not None:
			for channel in self.bot_channels:
				try:
					self.bolt.client.chat_postMessage(
						channel=channel.get('id'),
						text=f"Goodbye #{channel.get('name')}! I am shutting down."
					)
				except SlackApiError as e:
					self.slack_api_error(e)

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

	def events_with_arguments_listener(self, command, context, event, logger, payload, request:BoltRequest, response):
		logger.debug(inspect.currentframe().f_code.co_name)
		callback_args = locals()
		del(callback_args['self'])
		plugin_type:str = None
		if command is not None: plugin_type = "command"
		if event is not None: plugin_type = "event"
		text = get_bot_mention_text(context.get('bot_user_id'), payload.get('text'))
		keyword = text.split()[0] if text is not None else None
		for plugin in self.plugins:
			if plugin_type == plugin.type and keyword == plugin.keyword:
				arg_names = inspect.getfullargspec(plugin.callback).args
				plugin.callback(**build_required_kwargs(
					logger=logger,
					request=request,
					response=response,
					required_arg_names=arg_names,
					this_func=plugin.callback,
				))

	def global_middleware_listener(self, logger:logging.Logger, action, next, request, shortcut, view):
		if action is not None:
			action_id = action.get('action_id', None)
			if action_id == 'plugin_help':
				action['plugins'] = self.plugins
		next()
	pass