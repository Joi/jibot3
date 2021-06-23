from lib.database import SQLite, select_query, table_exists, create_table

from pathlib import Path
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient
import logging
import re
import sqlite3

table_name:str = Path(__file__).stem
if not table_exists(table_name):
	create_table(table_name, "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, URL text NOT NULL")

def blocks():
	blocks:list = [{
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": ":link: Shared Links"
		}
	}]
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

class action:
	def __init__(self, ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest):
		container = request.body.get('container', None)
		view:dict = request.body.get(container.get('type'))
		title:dict = view.get('title')
		title.update(text=":link: Links")
		close_button = view.get('close')
		close_button.update(text="Go Back")
		content:list = list()
		content.extend(blocks())
		client.views_push(
			trigger_id=request.body.get('trigger_id'),
			view={
				"type": view.get('type'),
				"title": title,
				"close": close_button,
				"blocks": content
			}
		)
		ack()
class message:
	__doc__ = "The bot will save any shared links that is sees. You can view this in the app home."
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
