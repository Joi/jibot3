import json
from lib.slack import get_bot_mention_text
from include.wikipedia import get_url as get_wikipedia_url
from include.zotero import Zotero

from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_bolt.context import BoltContext
from slack_bolt.kwargs_injection import build_required_kwargs
from slack_sdk.web import WebClient

import inspect
import logging

class event:
	__doc__ = "\n".join([
		"The following functions are available when you @mention the bot:",
		"`wikipedia [SEARCH TERM OR PHRASE]`",
		"`zotero [SEARCH TERM OR PHRASE]`",
		# etc
	])

	def __init__(self, ack:Ack, event:dict, client:WebClient, context:BoltContext, logger:logging.Logger, payload:dict, request:BoltRequest, response:BoltResponse):
		text = get_bot_mention_text(context.get('bot_user_id'), payload.get('text'))
		keyword, sep, payload_text = text.partition(" ")
		payload['text'] = payload_text
		if hasattr(self, keyword):
			event_handler = getattr(self, keyword)
			arg_names = inspect.getfullargspec(event_handler).args
			event_handler(**build_required_kwargs(
				logger=logger,
				request=request,
				response=response,
				required_arg_names=arg_names,
				this_func=event_handler,
			))

	def wikipedia(self, ack:Ack, context:BoltContext, logger:logging.Logger, payload:dict, say:Say):
		ack()
		wiki_url = get_wikipedia_url(payload.get('text'))
		if wiki_url: say(text=wiki_url)

	def zotero(self, ack:Ack, client:WebClient, context:BoltContext, logger:logging.Logger, payload:dict, say:Say):
		ack()
		search_term = payload.get('text')
		zotero = Zotero(context.get('bot_user_id'))
		results = zotero.read(search_term)
		if len(results):
			say(blocks=zotero.blocks(results))
		else:
			say(f"I did not find any zotero items matching `{search_term}`")