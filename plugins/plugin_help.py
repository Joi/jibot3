import json
from lib.plugin import Plugin
import logging
import os
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient
from lib.slack import slack_bot_slash_command as bot_slash_command

class action:
	def __init__(self, ack:Ack, action:dict, client:WebClient, context, logger:logging.Logger, payload:dict, request:BoltRequest):
		ack()
		container = request.body.get('container')
		view:dict = request.body.get(container.get('type'))
		plugin_help_content:list = []
		plugins = payload['plugins']
		if plugins is not None:
			for p in plugins:
				plugin:Plugin = p
				if plugin.callback.__doc__ is not None:
					plugin_help_content.append({
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": plugin.callback.__doc__
						}
					})
		title:dict = view.get('title')
		title.update(text="Plugin Info")
		close_button = view.get('close')
		close_button.update(text="Go Back")
		client.views_push(
			trigger_id=request.body.get('trigger_id'),
			view={
				"type": view.get('type'),
				"title": title,
				"close": close_button,
				"blocks": plugin_help_content
			}
		)