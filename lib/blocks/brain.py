import json
from lib.database import SQLite

blocks:list = []
_db:SQLite = SQLite()
_brain_query:str = "SELECT * FROM definition ORDER BY key ASC;"
_brain = _db.cursor.execute(_brain_query).fetchall()
if _brain is not None:
	for b in _brain:
		thing:str = b[0]
		definitions = json.loads(b[1])
		blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{thing}:* {', '.join(definitions)}"
			}
		})