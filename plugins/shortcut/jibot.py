import json
import logging
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_sdk.web import WebClient
def callback_function(ack: Ack, client:WebClient, context, logger:logging.Logger, shortcut:dict, request:BoltRequest):
	ack()
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
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Configuration options and settings things."
				},
				"accessory": {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Configuration",
						"emoji": True
					},
					"action_id": "bot_config",
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
					"action_id": "brain",
				}
			},
		]
	}
	client.views_open(
        trigger_id=shortcut["trigger_id"],
		view=json.dumps(view)
    )