import json
from lib.database import SQLite
from include.blocks.karma import get_blocks as get_karma
from include.blocks.brain import get_blocks as get_brain

def callback_function(ack, event, client, context):
	ack()
	view = event.get('view', None)
	view_id = view.get('id') if view is not None else None
	user_id = event["user"]
	app_home_view = {
		"type": "home",
		"blocks": [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Hi <@{user_id}>!* :clap: :raised_hands:"
			}
		}]
	}
	app_home_view['blocks'].extend(get_karma())
	app_home_view['blocks'].extend(get_brain())
	if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(app_home_view))
	else: client.views_update(view_id=view.get('id'), view=json.dumps(app_home_view))