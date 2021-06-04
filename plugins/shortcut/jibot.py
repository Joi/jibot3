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
		]
	}
	client.views_open(
        trigger_id=shortcut["trigger_id"],
		view=json.dumps(view)
    )