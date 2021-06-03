import json
import os
from slack_sdk.web import WebClient
def callback_function(ack, client:WebClient, logger, shortcut):
	ack()
	view = {
		"type": "modal",
		"title": {
			"type": "plain_text",
			"text": "Help",
			"emoji": True
		},
		"close": {
			"type": "plain_text",
			"text": "Close",
			"emoji": True
		},
		"blocks": []
	}
	plugins = shortcut.get('plugins')
	blocks = view.get('blocks')
	bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
	if plugins is not None:
		for plugin in plugins:
			if plugin.type == "action": continue
			if plugin.callback.__doc__ is not None:
				blocks.append({
					"type": "section",
					"text": {
						"type": "mrkdwn",
						# "text": f"{plugin.event_name} {plugin.keyword} {plugin.regex} {plugin.type}"
						"text": " ".join([
								f"*{plugin.event_name}* _{plugin.keyword}_" if plugin.event_name is not None and plugin.type != "command" else ""
								f"*/{bot_slash_command}* _{plugin.keyword}_" if plugin.type == "command" else f"*{plugin.type}* _{plugin.keyword}_" if plugin.event_name is None else "",
								f"\n {plugin.callback.__doc__}"
							])
					}
				})
	view = client.views_open(
        trigger_id=shortcut["trigger_id"],
		view=json.dumps(view)
    )