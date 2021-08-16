import ast
import glob
import inspect
import importlib
import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from lib.plugin import Plugin
from lib.logging import logger

whitespace:str = "|".join([' ', '\xa0'])
slack_app_token:str = os.environ.get("JIBOT_SLACK_APP_TOKEN", None)
slack_bot_token:str = os.environ.get("JIBOT_SLACK_BOT_TOKEN", None)
slack_bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
slack_client_id:str = os.environ.get("JIBOT_SLACK_CLIENT_ID", None)
slack_signing_secret:str = os.environ.get("JIBOT_SLACK_SIGNING_SECRET", None)
slack_port = int(os.environ.get("JIBOT_PORT", 3000))

def get_bot_mention_text(bot_id, text):
	if text is None: return text
	logger.debug(inspect.currentframe().f_code.co_name)
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

class jibot_slack_app:
	global 	slack_app_token, slack_bot_token, slack_bot_slash_command, slack_signing_secret, slack_port
	bolt:App = None
	app_dir:str = os.getcwd()
	plugins_dir:str = app_dir + os.sep +  'plugins'
	app_token:str = slack_app_token
	bot_token:str = slack_bot_token
	bot_slash_command:str = slack_bot_slash_command
	signing_secret:str = slack_signing_secret
	bot_user = None
	channels = None
	bot_channels:list = []
	users = None
	plugins:list = []
	event_types:list = [
		"action",
		"command",
		"event",
		"message",
		"shortcut",
        "view"
	]

	def __init__(self):
		logger.info("Initializing slack...")
		self.bolt = App(
			signing_secret = self.signing_secret,
			token = self.bot_token,
		)
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

	def load_plugins(self):
		logger.info("Loading slack plugins...")
		plugin_files = glob.glob(self.plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
		for plugin_path in plugin_files:
			relative_path = os.path.relpath(plugin_path, os.getcwd())
			import_path = relative_path.replace(".py", "").replace(os.sep, ".")
			for event_type in self.event_types:
				plugin = Plugin(event_type, importlib.import_module(import_path))
				if plugin.callback is not None:
					if hasattr(self.bolt, plugin.type):
						event_handler:callable = getattr(self.bolt, plugin.type)
						event_handler(plugin.keyword)(plugin.callback)
						self.plugins.append(plugin)

	def start(self):
		logger.info("Starting slack socket mode...")
		self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
		self.socket_mode.start()

	def close(self):
		logger.info("Disconnecting socket mode...")
		self.bot_says_bye()
		self.socket_mode.disconnect()

	def test_slack_client_connection(self):
		logger.info("Testing slack client connectivity...")
		try:
			self.bolt.client.api_test().get("ok")
			logger.info("Slack client OK.");
		except SlackApiError as e:
			logger.error("Unable to establish a slack web client connection!")
			self.slack_api_error(e)

	def who_is_bot(self):
		logger.info("Establishing bot presence...")
		try:
			bot_auth = self.bolt.client.auth_test(token=self.bot_token)
			self.bot_user = self.bolt.client.users_info(user=bot_auth.get("user_id")).get("user")
			logger.info("Bot OK");
			logger.debug(self.bot_user)
		except SlackApiError as e:
			self.slack_api_error(e)

	def bot_says_hi(self):
		logger.info("Announce bot presence in slack...")
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
		logger.info("Announce bot exit from slack...")
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
		logger.info("Get info about slack team, channels, etc...")
		if self.bot_user is not None:
			team_id = self.bot_user.get("team_id", None)
			try:
				self.team = self.bolt.client.team_info(team=team_id).get("team")
				self.channels = self.bolt.client.conversations_list().get('channels')
				self.users = self.bolt.client.users_list().get('members')
			except SlackApiError as e:
				self.slack_api_error(e)

	def global_middleware_listener(self, payload:dict, next):
		payload['plugins'] = self.plugins
		next()

	def slack_api_error(self, error: SlackApiError):
		error_name = error.response['error']
		assert(error_name)
		if error_name == 'missing_scope':
			missing_scope = error.response['needed']
			message = f"The bot is missing proper oauth scope!({missing_scope}). Scopes are added to your bot at https://api.slack.com/apps."
			logger.error(message)
		logger.error(error)
