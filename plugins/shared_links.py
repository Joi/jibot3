from lib.database import SQLite

from pathlib import Path
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient
import logging
import re
import sqlite3

table_name:str = Path(__file__).stem
table_params:str = "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, URL text NOT NULL"
SQLite().create_table(table_name, table_params)

class shared_links:
	db:SQLite
	select_query:str

	def __init__(self):
		self.db = SQLite()
		self.select_query = self.db.select_query(table_name, order_by="URL", order="ASC")

	def blocks(self):
		blocks:list = [{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":link: Shared Links"
			}
		}]
		links = self.db.cursor.execute(self.select_query).fetchall()
		if links is not None:
			for l in links:
				url:str = l[1]
				blocks.append({
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": url
					},
				})
		return(blocks)

class action(shared_links):
	def __init__(self, ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest):
		super().__init__()
		container = request.body.get('container', None)
		view:dict = request.body.get(container.get('type'))
		title:dict = view.get('title')
		title.update(text=":link: Links")
		close_button = view.get('close')
		close_button.update(text="Go Back")
		content:list = list()
		content.extend(self.blocks())
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

class message(shared_links):
	__doc__ = "The bot will save any shared links that is sees."
	keyword:re = re.compile("(\w+:\/\/[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\[\]`#|]+)", re.IGNORECASE)

	def __init__(self, logger:logging.Logger, payload:dict):
		super().__init__()
		matches:list = self.keyword.findall(payload.get('text'))
		if matches is not None:
			for url in matches:
				logger.info(f"Saving link: {url}")
				try:
					self.db.cursor.execute(f"INSERT INTO {table_name} (URL) VALUES(?)", (url,))
					self.db.connection.commit()
				except sqlite3.Error as e:
					logger.error(e)
