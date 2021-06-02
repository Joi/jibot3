import json
from lib.database import SQLite
def callback_function(ack, event, client, context):
	ack()
	view = event.get('view', None)
	view_id = view.get('id') if view is not None else None
	user_id = event["user"]
	view_blocks = {
		"type": "home",
		"blocks": [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Hi <@{user_id}>!* :clap: :raised_hands:"
			}
		}]
	}
	blocks:list = view_blocks['blocks']
	db:SQLite = SQLite()
	karma_karma_karma_karma_karma_queryaaaaa:str = "SELECT * FROM karma ORDER BY key ASC;"
	karma = db.cursor.execute(karma_karma_karma_karma_karma_queryaaaaa).fetchall()
	if karma is not None:
		blocks.append({"type": "divider"},)
		blocks.append({
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
			blocks.append({
				"type": "section",
				"fields": [
					{
						"type": "mrkdwn",
						"text": f"{emoji} *{word}: {total_score}* `(+{plusses}/-{minuses})`"
					}
				],

			})
	brain_query:str = "SELECT * FROM definition ORDER BY key ASC;"
	brain = db.cursor.execute(brain_query).fetchall()
	if brain is not None:
		blocks.append({"type": "divider"},)
		blocks.append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":brain: Brains",
				"emoji": True
			}
		})
		for b in brain:
			thing:str = b[0]
			definitions = json.loads(b[1])
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "\n".join([
						f"*{thing}:* {', '.join(definitions)}"
					]),
				}
			})
	if view_id is None: client.views_publish(user_id=context.get('user_id'),view=json.dumps(view_blocks))
	else: client.views_update(view_id=view.get('id'), view=json.dumps(view_blocks))