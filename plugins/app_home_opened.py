from plugins.shared_links import shared_links
from plugins.user_likes import user_likes
from plugins.user_dislikes import user_dislikes

from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
import json

class event:
	def __init__(self, ack:Ack, event:dict, client:WebClient, context: BoltContext):
		ack()
		view = event.get('view', None)
		view_id = view.get('id') if view is not None else None
		user_id = event["user"]
		user_response:SlackResponse = client.users_info(user=user_id)
		user = user_response.get('user') if user_response.get('ok') else None
		app_home_view = {
			"type": "home",
			"blocks": [{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"*Hello <@{user_id}>!* :clap: :raised_hands: Welcome!"
				}
			}]
		}
		if user.get('is_admin') or user.get('is_owner'):
			if user.get('is_admin'):
				app_home_view['blocks'].extend([
					{
						"type": "section",
						"text": {
							"type": "plain_text",
							"text": ":wave: Hello operator!",
							"emoji": True
						}
					},
				])
			if user.get('is_owner'):
				app_home_view['blocks'].extend([
					{
						"type": "section",
						"text": {
							"type": "plain_text",
							"text": ":wave: Hello owner!",
							"emoji": True
						}
					},
				])
		app_home_view['blocks'].extend(user_likes().blocks(user_id))
		app_home_view['blocks'].extend(user_dislikes().blocks(user_id))
		app_home_view['blocks'].extend(shared_links().blocks())
		if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(app_home_view))
		else: client.views_update(view_id=view.get('id'), view=json.dumps(app_home_view))