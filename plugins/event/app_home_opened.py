import json
from lib.database import SQLite
def callback_function(event, client, context, request):
	view = event.get('view', None)
	view_id = view.get('id') if view is not None else None
	user_id = event["user"]
	view_blocks = {
		"type": "home",
		"blocks": [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Hi <@{user_id}>!* :clap: :raised_hands: This code is running from: {__file__}!!!!"
			}
		}]
	}
	db:SQLite = SQLite()
	karma_karma_karma_karma_karma_queryaaaaa:str = "SELECT * FROM karma;"
	karma = db.cursor.execute(karma_karma_karma_karma_karma_queryaaaaa).fetchall()
	if karma is not None:
		view_blocks['blocks'].append({"type": "divider"},)
		view_blocks['blocks'].append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":scales: Karma",
				"emoji": True
			}
		})
		for k in karma:
			word:str = k[0]
			plusses:int = k[1]
			minuses:int = k[2]
			total_score = plusses - minuses

			emoji:str = ":yin_yang:"
			if total_score > 0: emoji = ":thumbsup:"
			if total_score < 0: emoji = ":thumbsdown:"
			view_blocks['blocks'].append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "\n".join([
						f"*{word}* {emoji} *{total_score}* `(+{plusses}/-{minuses})`"
					])
				}
			})
	brain_query:str = "SELECT KEY, json(DEFS) FROM definition;"
	brain = db.cursor.execute(brain_query).fetchall()
	if brain is not None:
		view_blocks['blocks'].append({"type": "divider"},)
		view_blocks['blocks'].append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":brain: Brains",
				"emoji": True
			}
		})
		for b in brain:
			thing:str = b[0]
			definitions = list(json.loads(b[1]))
			view_blocks['blocks'].append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "\n".join([
						f"*{thing}*",
						", ".join(definitions)
					])
				}
			})
	if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(view_blocks))
	else: client.views_update(view_id=view.get('id'), view=json.dumps(view_blocks))