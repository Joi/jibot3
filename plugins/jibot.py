from include.wikipedia import get_url as get_wikipedia_url

import inspect
import json
import logging

from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond
from slack_bolt.kwargs_injection import build_required_kwargs
from slack_sdk.web import WebClient

class command:
	keyword = f"/{Path(__file__).stem}"
	__doc__ = "\n".join([
		f"The following functions are examples of available bot slash commands:",
		f"`{keyword} wikipedia [SEARCH TERM OR PHRASE]`",
		f"`{keyword} hello_world`",
		# etc
	])
	def __init__(self, ack:Ack, logger:logging.Logger, payload:dict, request:BoltRequest, response: BoltResponse):
		keyword = payload.get('text').split()[0]
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
			ack()

	def wikipedia(self, payload:dict, respond:Respond):
		search_term = payload.get('text')
		search_result = get_wikipedia_url(search_term)
		respond(search_result)

	def hello_world(self, payload:dict, respond:Respond):
		respond(f"HELLO <@{payload['user_id']}> :wave: !")

class shortcut:
	def __init__(self, ack:Ack, client:WebClient, shortcut:dict):
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
			"blocks": [
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
				},
				# {
				# 	"type": "section",
				# 	"text": {
				# 		"type": "mrkdwn",
				# 		"text": "Configuration options and settings things."
				# 	},
				# 	"accessory": {
				# 		"type": "button",
				# 		"text": {
				# 			"type": "plain_text",
				# 			"text": "Configuration",
				# 			"emoji": True
				# 		},
				# 		"action_id": "bot_config",
				# 	}
				# },
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Huzzah Zotero"
					},
					"accessory": {
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Zotero Integration",
							"emoji": True
						},
						"action_id": "zotero_config",
					}
				},
				{
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
				},
				{
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
				},
				{
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
				},
			]
		}
		client.views_open(
			trigger_id=shortcut["trigger_id"],
			view=json.dumps(view)
		)