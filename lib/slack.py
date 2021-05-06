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

class app:
	app_token = os.environ.get("JIBOT_SLACK_APP_TOKEN", None)
	bot_token = os.environ.get("JIBOT_SLACK_BOT_TOKEN", None)
	client_id = os.environ.get("JIBOT_SLACK_CLIENT_ID", None)
	client_secret = os.environ.get("JIBOT_SLACK_CLIENT_SECRET", None)
	signing_secret = os.environ.get("JIBOT_SLACK_SIGNING_SECRET", None)
	user_token = os.environ.get("JIBOT_SLACK_USER_TOKEN", None)
	verification_token = os.environ.get("JIBOT_SLACK_VERIFICATION_TOKEN", None)
	port = int(os.environ.get("JIBOT_PORT", 3000))

	ngrok_token = os.environ.get("JIBOT_NGROK_AUTH_TOKEN", None)
	ngrok_hostname = os.environ.get("JIBOT_NGROK_HOSTNAME", None)
	has_ngrok:bool = True if ngrok_token is not None else False
	do_socket_mode:bool = ast.literal_eval(os.environ.get("JIBOT_DO_SOCKET_MODE", 'True'))
	api_connected:bool = False
	bot_user = None
	user = None
	users = None
	channels = None
	webhook = WebhookClient("https://hooks.slack.com/services/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")

	def __init__(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		self.bolt = App(
			name="jibot",
			signing_secret = self.signing_secret,
			token = self.bot_token,
			raise_error_for_unhandled_request = False,
			verification_token = self.verification_token
		)
		self.bolt.use(self.global_listener)
		self.test_slack_client_connection()
		self.who_am_i()
		self.who_made_me()
		self.where_am_i()
		self.what_channels_am_i_on()
		self.who_is_here()
		self.start()



	def slack_api_error(self, error: SlackApiError):
		error_name = error.response['error']
		assert(error_name)
		if error_name == 'missing_scope':
			missing_scope = error.response['needed']
			logging.error(f"The bot is missing proper oauth scope!({missing_scope}). Scopes are added to your bot at https://api.slack.com/apps.")
		logging.error(error.response)

	def load_plugins(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		app_dir = os.getcwd()
		plugins_dir = app_dir + os.sep +  'plugins'
		plugin_files = glob.glob(plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
		path_regex = re.compile("^plugins\/(\w+)\/(.+)\.py$")
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
					logging.info(f"This plugin has a keyword specified ('{keyword}'), this overrides using the plugin filename as the keyword.")
				except AttributeError as e:
					assert(e)
				if plugin.get('type') == 'command' and keyword.startswith('/') is not True:
					keyword = f"/{keyword}"
				callback_function:callable = plugin.get('lib').callback_function
				handler_function:callable = getattr(self.bolt, plugin.get('type'))
				handler_function(keyword)(callback_function)

	def start(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		if self.do_socket_mode is True:
			self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
			logging.info("Starting bolt app in Socket mode....")
			self.socket_mode.start()

		else:
			if (self.has_ngrok is True):
				logging.info("Detected ngrok... starting request url tunnel...")
				request_url_tunnel = ngrok.connect(self.port, "http", subdomain=self.ngrok_hostname)
				ngrok_process = ngrok.get_ngrok_process()
				logging.info("Request Url is: " + request_url_tunnel.public_url)
			self.bolt.start(port=self.port)

	def close(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		if (self.has_ngrok is True):
			ngrok.kill()

	def test_slack_client_connection(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		try:
			self.api_connected = self.bolt.client.api_test().get("ok")
			logging.info("Slack web client connection established...")
		except SlackApiError as e:
			logging.error("Unable to establish a slack web client connection!")
			self.slack_api_error(e)

	def who_am_i(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		try:
			bot_auth = self.bolt.client.auth_test(token=self.bot_token)
			self.bot_user = self.bolt.client.users_info(user=bot_auth.get("user_id")).get("user")
			logging.info(f"Hello, I am bot. My name is {self.bot_user.get('real_name')}. I am waking up.")
			logging.info(self.bolt)
			logging.debug(self.bot_user)
		except SlackApiError as e:
			self.slack_api_error(e)

	def where_am_i(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		if self.bot_user is not None:
			team_id = self.bot_user.get("team_id", None)
			try:
				self.team = self.bolt.client.team_info(team=team_id).get("team")
				logging.info(f"I am on slack team named {self.team.get('name')}.")
				logging.debug(self.team)
			except SlackApiError as e:
				self.slack_api_error(e)
		try:
			self.channels = self.bolt.client.conversations_list().get('channels')
			logging.info(f"There are {len(self.channels)} channels.")
		except SlackApiError as e:
			self.slack_api_error(e)

	def who_is_here(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		try:
			self.users = self.bolt.client.users_list().get('members')
			logging.info(f"There are {len(self.users)} users.")
			logging.debug(self.users)
		except SlackApiError as e:
			self.slack_api_error(e)

	def who_made_me(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		if (self.user_token is not None):
			try:
				user_auth = self.bolt.client.auth_test(token=self.user_token)
				self.user = self.bolt.client.users_info(user=user_auth.get("user_id")).get("user")
				logging.info(f"I was installed here by {self.user.get('real_name')}.")
				logging.debug(self.user)
			except SlackApiError as e:
				self.slack_api_error(e)

	def what_channels_am_i_on(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		bot_channels:list = []
		for channel in self.channels:
			try:
				channel_members =  self.bolt.client.conversations_members(channel=channel.get('id')).get('members')
				if self.bot_user is not None and self.bot_user.get('id') in channel_members:
					bot_channels.append(channel.get('id'))
					logging.info(f"I am on #{channel.get('name')}. I should say hello.")

					self.webhook.send(text=f"I am waking up.")
					# response = webhook.send(text="Hello!")
					# self.bolt.client.chat_postMessage(
					# 	channel=channel.get('id'),
					# 	text=f"Hello #{channel.get('name')}! I am {self.bot_user.get('real_name')}. I am waking up."
					# )
			except SlackApiError as e:
				self.slack_api_error(e)
		if len(bot_channels) == 0:
			logging.warning("The bot is NOT on any slack channels. Should we consider having the bot create a channel (if scopes allow)? You can also add bot to a channel via @mention_bot_name")

	def global_listener(self, ack, action, client, command, context, event, logger, message, next, options, payload, request, response, respond, say, shortcut, view):
		logger.info("+++++++" + inspect.currentframe().f_code.co_name + "+++++++")
		if command is not None:
			ack()

		next()
		logger.debug(payload)
	pass