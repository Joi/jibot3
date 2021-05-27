import json
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
	if plugins is not None:
		for plugin in plugins:
			plugin_type = plugin.get('type', None)
			if plugin_type == "action": continue
			keyword:str = plugin.get('keyword', None)
			event_name:str = plugin.get('event_name', '')
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{plugin_type} {event_name} {keyword}"
				}
			})
	view = client.views_open(
        trigger_id=shortcut["trigger_id"],
		view=json.dumps(view)
    )