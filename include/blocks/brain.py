import json
from lib.database import SQLite
def get_blocks():
	blocks:list = []
	db:SQLite = SQLite()
	brain_query:str = "SELECT * FROM definition ORDER BY key ASC;"
	brain = db.cursor.execute(brain_query).fetchall()
	if brain is not None:
		for b in brain:
			thing:str = b[0]
			definitions = json.loads(b[1])
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"*{thing}:* {', '.join(definitions)}"
				}
			})
	return(blocks)