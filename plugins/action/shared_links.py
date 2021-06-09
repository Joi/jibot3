import logging
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient
from include.shared_links import blocks as get_shared_links

def callback_function(ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest):
	container = request.body.get('container', None)
	view:dict = request.body.get(container.get('type'))
	title:dict = view.get('title')
	title.update(text=":link: Links")
	close_button = view.get('close')
	close_button.update(text="Go Back")
	content:list = list()
	content.extend(get_shared_links())
	client.views_push(
		trigger_id=request.body.get('trigger_id'),
		view={
			"type": view.get('type'),
			"title": title,
			"close": close_button,
			"blocks": content
		}
	)
	ack()