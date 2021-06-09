import json
from lib.database import SQLite

from include.user_likes import blocks as user_likes
from include.karma import blocks as karma
# from include.blocks.karma import get_blocks as get_karma
# from include.blocks.brain import get_blocks as get_brain
# from include.herald import blocks as herald_blocks


from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

def callback_function(ack:Ack, body:dict, event:dict, client:WebClient, context: BoltContext, payload:dict, request:BoltRequest):
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
				"text": f"*Hi <@{user_id}>!* :clap: :raised_hands:"
			}
		}]
	}
	app_home_view['blocks'].extend(user_likes(user_id))
	# app_home_view['blocks'].extend(karma())

	# if user.get('is_admin') or user.get('is_owner'):
	# 	if user.get('is_admin'):
	# 		app_home_view['blocks'].extend([
	# 			{
	# 				"type": "section",
	# 				"text": {
	# 					"type": "plain_text",
	# 					"text": ":wave: Hello operator!",
	# 					"emoji": True
	# 				}
	# 			},
	# 		])
	# 	if user.get('is_owner'):
	# 		app_home_view['blocks'].extend([
	# 			{
	# 				"type": "section",
	# 				"text": {
	# 					"type": "plain_text",
	# 					"text": ":wave: Hello owner!",
	# 					"emoji": True
	# 				}
	# 			},
	# 		])
	# app_home_view['blocks'].append({
	# 	"type": "header",
	# 	"text": { "type": "plain_text", "text": ":yin_yang: Karma" }
	# })
	# app_home_view['blocks'].extend(get_karma())
	# app_home_view['blocks'].append({
	# 	"type": "header",
	# 	"text": { "type": "plain_text", "text": ":brain: Brains" }
	# })
	# app_home_view['blocks'].extend(get_brain())
	if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(app_home_view))
	else: client.views_update(view_id=view.get('id'), view=json.dumps(app_home_view))