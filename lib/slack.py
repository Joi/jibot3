import os
import logging
from logging import Logger
from typing import Callable, Dict, Any, Optional

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient

class EventListener():
	def __init__(self, callback_function):
		self.callback_function = callback_function

	def __call__(
		self,
		action,
		command,
		event,
		options,
		shortcut,
		view,

		client: WebClient,		# slack_sdk.web.WebClient instance with a valid token
		context: BoltContext,	# Context data associated with the incoming request
		body: Dict[str, Any],	# Parsed request body data
		logger: Logger,
		request: BoltRequest,
		req: BoltRequest,
		response: BoltResponse,
		resp: BoltResponse,
		ack: Ack,					# returns acknowledgement to the Slack servers
		respond: Respond,			# utilizes the associated response_url
		say: Say,					# calls chat.postMessage API with the associated channel ID
		next: Callable[[], None],	# tells the middleware chain that it can continue with the next one
		payload: Dict[str, Any],
	):
		if (ack):
			ack()
		self.callback_function(payload, say)
class app:
	def __init__(self, **args):
		self.bolt = App(
			token = args.get('token'),
			signing_secret = args.get('signing_secret')
		)
		self.socket_mode = SocketModeHandler(self.bolt, args.get('app_token'))

	def __call__(self, event_type, keyword, callback_function):
		self.event_type = event_type
		self.keyword = keyword
		self.callback_function = callback_function
		self.handler_function = getattr(self.bolt, self.event_type)
		self.handler_function(self.keyword)(EventListener(callback_function))
	pass