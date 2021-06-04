import json
import logging
import os
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient

def callback_function(ack:Ack, action:dict, client:WebClient, context, logger:logging.Logger, request:BoltRequest):
	ack()
	container = request.body.get('container')
	view:dict = request.body.get(container.get('type'))
	title:dict = view.get('title')
	title.update(text="Configuration")
	client.views_update(
		view_id=view.get('id'),
		view={
			"type": view.get('type'),
			"title": title,
			"close": view.get('close'),
			"blocks": [
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": "Coming Soon!"
					}
				},
			]
		}
	)