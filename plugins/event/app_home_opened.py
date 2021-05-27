import json
def callback_function(event, client):
	view = event.get('view', None)
	view_id = view.get('id') if view is not None else None
	user_id = event["user"]
	view_blocks = {
		"type": "home",
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"*Hi <@{user_id}>!* :clap: :raised_hands: This code is running from: {__file__}"
				}
			},
		]
	}
	if view_id is None: client.views_publish(view=json.dumps(view_blocks))
	else: client.views_update(view_id=view.get('id'), view=json.dumps(view_blocks))