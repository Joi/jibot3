from lib.database import SQLite, select_query, table_exists, create_table

from pathlib import Path
import logging
import re
import sqlite3

table_name:str = Path(__file__).stem
if not table_exists(table_name):
	create_table(table_name, "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, URL text NOT NULL")

def blocks():
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

class message:
	keyword:re = re.compile("(\w+:\/\/[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\[\]`#|]+)", re.IGNORECASE)
	def __init__(self, logger:logging.Logger, payload:dict):
		db:SQLite = SQLite()
		matches:list = self.keyword.findall(payload.get('text'))
		if matches is not None:
			for url in matches:
				logger.info(f"Saving link: {url}")
				try:
					db.cursor.execute(f"INSERT INTO {table_name} (URL) VALUES(?)", (url,))
					db.connection.commit()
				except sqlite3.Error as e:
					logger.error(e)
