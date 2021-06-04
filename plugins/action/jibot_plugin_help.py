import json
import logging
import os
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient

def callback_function(ack:Ack, action:dict, client:WebClient, context, logger:logging.Logger, request:BoltRequest):
	ack()
	container = request.body.get('container')
	view:dict = request.body.get(container.get('type'))
	plugins = action.get('plugins', None)
	bot_slash_command:str = os.environ.get("JIBOT_SLACK_SLASH_COMMAND", None)
	plugin_help_content:list = []
	if plugins is not None:
		for plugin in plugins:
			if plugin.type == "action": continue
			if plugin.callback.__doc__ is not None:
				plugin_help_content.append({
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": " ".join([
								f"*{plugin.event_name}* _{plugin.keyword}_" if plugin.event_name is not None and plugin.type != "command" else ""
								f"*/{bot_slash_command}* _{plugin.keyword}_" if plugin.type == "command" else f"*{plugin.type}* _{plugin.keyword}_" if plugin.event_name is None else "",
								f"\n {plugin.callback.__doc__}"
							])
					}
				})

	title:dict = view.get('title')
	title.update(text="Plugin Info")
	client.views_update(
		view_id=view.get('id'),
		view={
			"type": view.get('type'),
			"title": title,
			"close": view.get('close'),
			"blocks": plugin_help_content
		}
	)