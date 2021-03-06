from slack_bolt.context.context import BoltContext
from slack_bolt.context.say.say import Say

from include.herald import herald
from include.wikipedia import get_url as get_wikipedia_url
from include.zotero import Zotero

import inspect
import json
import logging

from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond
from slack_bolt.kwargs_injection import build_required_kwargs
from slack_sdk.web import WebClient, slack_response

class command:
	keyword = f"/{Path(__file__).stem}"
	__doc__ = "\n".join([
		f"The following functions are examples of available bot slash commands:",
		f"`{keyword} hello_world`",
		f"`{keyword} wikipedia [SEARCH TERM OR PHRASE]`",
		f"`{keyword} zotero [SEARCH TERM OR PHRASE]`",
		f"`{keyword} herald [me|@user]`",
		# etc
	])

	def __init__(self, ack:Ack, context:BoltContext, logger:logging.Logger, payload:dict, request:BoltRequest, respond: Respond, response: BoltResponse):
		self.herald = herald
		keyword, sep, payload_text = payload.get('text').partition(" ")
		payload['text'] =  payload_text
		if keyword:
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
		else:
			ack()
			respond(self.__doc__)


	def hello_world(self, ack: Ack, payload:dict, respond:Respond):
		ack()
		respond(f"HELLO <@{payload['user_id']}> :wave: !")

	def wikipedia(self, ack: Ack, payload:dict, respond:Respond):
		ack()
		search_term = payload.get('text')
		result = get_wikipedia_url(search_term)
		respond(result)

	def zotero(self, ack: Ack, client:WebClient, command:dict, context:BoltContext, payload:dict, respond:Respond, say:Say):
		ack()
		user_id:str = context.get('user_id')
		search_term = payload.get('text')
		zotero = Zotero(user_id)
		results = zotero.read(search_term)
		if len(results):
			respond(blocks=zotero.blocks(results))
		else:
			respond(f"I did not find any zotero items matching `{search_term}`")

class shortcut:
	def __init__(self, ack:Ack, context:BoltContext, client:WebClient, shortcut:dict):
		ack()
		user_id = context.get('user_id')
		user_response:slack_response = client.users_info(user=user_id)
		user = user_response.get('user') if user_response.get('ok') else None
		view = {
			"type": "modal",
			"title": {
				"type": "plain_text",
				"text": "Jibot Info and Help",
				"emoji": True
			},
			"close": {
				"type": "plain_text",
				"text": "Close",
				"emoji": True
			},
			"blocks": []
		}
		view["blocks"].append(
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Get information and syntax help for installed plugins."
				},
				"accessory": {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Plugin Help",
						"emoji": True
					},
					"action_id": "plugin_help",
				}
			}
		)
		view["blocks"].append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "View a list of links which have been shared."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "View Links",
					"emoji": True
				},
				"action_id": "shared_links",
			}
		})
		view["blocks"].append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Karma karma karma karma karma queryaaaah!"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "View Karma",
					"emoji": True
				},
				"action_id": "karma",
			}
		})
		view["blocks"].append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "The bot tries to learn, check out it's brain."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "View Brains",
					"emoji": True
				},
				"action_id": "definition",
			}
		})

		view["blocks"].append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Connect your Zotero Account to Slack"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Zotero Config",
					"emoji": True
				},
				"action_id": "zotero",
			}
		})

		client.views_open(
			trigger_id=shortcut["trigger_id"],
			view=json.dumps(view)
		)