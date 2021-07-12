import inspect
import logging

from slack_bolt.kwargs_injection.utils import build_required_kwargs
from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse
from plugins.shared_links import shared_links
from include.herald import herald

from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
import json

class event:
	def __init__(self, ack:Ack, context: BoltContext, client:WebClient, event:dict, logger:logging.Logger, payload:dict, request:BoltRequest, response:BoltResponse):
		ack()
		view = event.get('view', None)
		view_id = view.get('id') if view is not None else None
		herald_function = herald(**build_required_kwargs(
			logger=logger,
			request=request,
			response=response,
			required_arg_names=inspect.getfullargspec(herald).args,
			this_func=herald,
		))
		app_home_view = {
			"type": "home",
			"blocks": herald_function.blocks()
		}
		app_home_view['blocks'].append({ "type": "divider" })
		app_home_view['blocks'].extend(shared_links().blocks())
		if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(app_home_view))
		else: client.views_update(view_id=view.get('id'), view=json.dumps(app_home_view))