import os
import logging
from logging import Logger
from typing import Callable, Dict, Any, Optional

# from pyngrok import ngrok

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient

class app:
	def __init__(self):
		self.do_socket_mode = False
		self.app_token = os.environ.get("SLACK_APP_TOKEN")
		self.bot_token = os.environ.get("SLACK_BOT_TOKEN")
		self.signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
		self.bolt = App(
			signing_secret = self.signing_secret,
			token = self.bot_token,
			raise_error_for_unhandled_request = False,
		)
		self.socket_mode = SocketModeHandler(self.bolt, self.app_token)

	def start(self, **kwargs):
		if kwargs.get("socket_mode"):
			self.do_socket_mode = kwargs.get("socket_mode")
		self.bolt.use(self.global_listener)
		if self.do_socket_mode is True:
			self.socket_mode.start()
		else:
			# ssh_tunnel = ngrok.connect(22, "tcp")
			# http_tunnel = ngrok.connect()
			self.bolt.start(port=int(os.environ.get("PORT", 3000)))

	def global_listener(self, client, context, logger, payload, next):
		logger.info(payload)
		next()

	def event_listener(self, event_type, keyword, callback_function):
		self.event_type = event_type
		self.keyword = keyword
		self.callback_function = callback_function
		self.handler_function = getattr(self.bolt, self.event_type)
		self.handler_function(self.keyword)(callback_function)
	pass