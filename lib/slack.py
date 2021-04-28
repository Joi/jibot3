import os
import logging
from logging import Logger
from typing import Callable, Dict, Any, Optional
from pyngrok import ngrok

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

class app:
	def __init__(self):
		self.do_socket_mode = True
		self.webhook = None
		self.ngrok = False
		self.ngrok_hostname = None
		if os.environ.get('NGROK_AUTH_TOKEN'):
			self.do_socket_mode = False
			self.ngrok = True
			self.ngrok_auth_token = os.environ.get('NGROK_AUTH_TOKEN')
			ngrok.set_auth_token(self.ngrok_auth_token)
			if os.environ.get('NGROK_HOSTNAME'):
				self.ngrok_hostname = os.environ.get('NGROK_HOSTNAME')
		self.port = int(os.environ.get("PORT", 3000))
		self.app_token = os.environ.get("SLACK_APP_TOKEN")
		self.bot_token = os.environ.get("SLACK_BOT_TOKEN")
		self.signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
		self.bolt = App(
			signing_secret = self.signing_secret,
			token = self.bot_token
		)
		self.socket_mode = SocketModeHandler(self.bolt, self.app_token)

	def start(self, **kwargs):
		self.bolt.use(self.global_listener)
		if kwargs.get("socket_mode"):
			self.do_socket_mode = kwargs.get("socket_mode")
		if self.do_socket_mode is True:
			self.socket_mode.start()
		else:
			if (self.ngrok is True):
				request_url_tunnel = ngrok.connect(self.port, "http", subdomain=self.ngrok_hostname)
				print("Request Url is: " + request_url_tunnel.public_url)
			self.bolt.start(port=self.port)


	def close(self):
		if (self.ngrok is True):
			ngrok.kill()

	def global_listener(self, client, context, logger, payload, next):
		print(payload)
		next()

	def create_event_listener(self, event_type, keyword, callback_function):
		self.event_type = event_type
		self.keyword = keyword
		self.callback_function = callback_function
		self.handler_function = getattr(self.bolt, self.event_type)
		self.handler_function(self.keyword)(callback_function)
	pass