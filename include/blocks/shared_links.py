from pathlib import Path
from lib.database import SQLite
def get_blocks():
	blocks:list = []
	db:SQLite = SQLite()
	table_name = Path(__file__).stem
	shared_links_query:str = f"SELECT * FROM {table_name} ORDER BY URL ASC;"
	links = db.cursor.execute(shared_links_query).fetchall()
	if links is not None:
		for l in links:
			id:int = l[0]
			url:str = l[1]
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": url
				},
			})
	return(blocks)