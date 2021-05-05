import inspect
from logging import Logger
import logging
import os
from pyngrok import ngrok

from slack_bolt import App
from slack_bolt.error import BoltError
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.authorization import  AuthorizeResult
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError

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
	has_ngrok = True if ngrok_token is not None else False

	do_socket_mode = False if has_ngrok is True else True
	api_connected:bool = False
	bot_user = None
	user = None
	users = None
	channels = None

	def __init__(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		self.bolt = App(
			name="jibot",
			signing_secret = self.signing_secret,
			token = self.bot_token,
			raise_error_for_unhandled_request = False
		)
		self.bolt.use(self.global_listener)
		self.test_slack_client_connection()
		self.who_am_i()
		self.who_made_me()
		self.where_am_i()
		self.who_is_here()
		self.what_channels_am_i_on()

	def slack_api_error(self, error: SlackApiError):
		error_name = error.response['error']
		if error_name == 'missing_scope':
			missing_scope = error.response['needed']
			logging.error(f"The bot is missing proper oauth scope!({missing_scope})")
		logging.error(error.response)

	def start(self, **kwargs):
		logging.debug(inspect.currentframe().f_code.co_name)
		self.do_socket_mode = kwargs.get("socket_mode", self.do_socket_mode)
		if self.do_socket_mode is True:
			self.socket_mode = SocketModeHandler(self.bolt, self.app_token)
			self.socket_mode.start()
			logging.info("Bolt app is running in Socket mode.")
		else:
			if (self.has_ngrok is True):
				logging.info("Detected ngrok... starting request url tunnel...")
				request_url_tunnel = ngrok.connect(self.port, "http", subdomain=self.ngrok_hostname)
				logging.info("Request Url is: " + request_url_tunnel.public_url)
			self.bolt.start(port=self.port)

	def close(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		if (self.has_ngrok is True):
			ngrok.kill()

	def create_event_listener(self, event_type, keyword, callback_function):
		self.event_type = event_type
		self.keyword = keyword
		self.callback_function = callback_function
		self.handler_function = getattr(self.bolt, self.event_type)
		self.handler_function(self.keyword)(callback_function)

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
		bot_auth = self.bolt.client.auth_test(token=self.bot_token)
		try:
			self.bot_user = self.bolt.client.users_info(user=bot_auth.get("user_id")).get("user")
			logging.info(f"Hello, I am bot. My name is {self.bot_user.get('real_name')}.")
			logging.debug(self.bot_user)
		except SlackApiError as e:
			self.slack_api_error(e)

	def where_am_i(self):
		logging.debug(inspect.currentframe().f_code.co_name)
		team_id = self.bot_user.get("team_id")
		try:
			self.team = self.bolt.client.team_info(team=team_id).get("team")
			logging.info(f"I am on slack team named '{self.team.get('name')}'.")
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
		user_auth = self.bolt.client.auth_test(token=self.user_token)
		try:
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
				if self.bot_user.get('id') in channel_members:
					bot_channels.append(channel.get('id'))
					logging.info(f"I am on #{channel.get('name')}. I should say hello.")
					self.bolt.client.chat_postMessage(
						channel=channel.get('id'),
						text=f"Hello #{channel.get('name')}! I am {self.bot_user.get('real_name')}."
					)
			except SlackApiError as e:
				self.slack_api_error(e)
		if len(bot_channels) == 0:
			logging.warning("The bot is NOT on any slack channels. Should we consider having the bot create a channel (if scopes allow)?")

	def global_listener(self, client, context, logger, payload, next):
		logging.debug(inspect.currentframe().f_code.co_name)
		logging.debug(payload)
		next()

	pass