from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_sdk.web import WebClient
def callback_function(ack:Ack, client:WebClient, logger, request:BoltRequest):
	ack()
	container = request.body.get('container')
	view = request.body.get(container.get('type'))
	client.views_update(view_id=view.get('id'), view={
		"type": view.get('type'),
		"title": view.get('title'),
		"close": view.get('close'),
		"blocks": [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Thank you for clicking!* :clap: :raised_hands: This code is running from: {__file__}"
			}
		}]
	})