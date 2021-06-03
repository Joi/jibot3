import os
from slack_bolt import Ack, BoltContext, BoltRequest, BoltResponse, Respond, Say
from slack_sdk.web import WebClient
def callback_function(ack:Ack, client:WebClient, context:BoltContext, logger, payload, request:BoltRequest, response:BoltResponse, respond:Respond, say:Say, shortcut):
	ack()
	user_id = shortcut.get('user_id')
	relative_path = os.path.relpath(__file__, os.getcwd())
	view = client.views_open(
        trigger_id=shortcut["trigger_id"],
		view={
			"type": "modal",
            "title": {"type": "plain_text", "text": "Hello World!"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hello world!"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"HELLO WORLD (and you, <@{user_id}>)! This code is running from: {relative_path}"
                        }
                    ]
                },
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "This is a section block with a button, and the button has an `action_id` and calls the callback function defined in `plugins/action/action_id.py`"
					},
					"accessory": {
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Click Me",
							"emoji": True
						},
						"value": shortcut["trigger_id"],
						"action_id": "hello_world"
					}
				}
            ]
        }
    )