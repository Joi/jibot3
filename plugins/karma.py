from lib.database import SQLite
from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_sdk.web import WebClient
import logging
import re
import sqlite3

plusplus:str = "\+\+"
minusminus:str = "--"

table_name:str = Path(__file__).stem
table_params:str = "key text PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0"
SQLite().create_table(table_name, table_params)

class karma:
	db:SQLite
	select_query:str

	def __init__(self):
		self.db = SQLite()
		self.select_query = self.db.select_query(table_name)

	def blocks(self):
		blocks:list = []
		karma_karma_karma_karma_karma_queryaaaaa:str = self.select_query
		karma = self.db.cursor.execute(karma_karma_karma_karma_karma_queryaaaaa).fetchall()
		if karma is not None:
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
					"text": {
						"type": "mrkdwn",
						"text": f"{emoji} *{word}: {total_score}* `(+{plusses}/-{minuses})`"
					},
				})
		return(blocks)

class action(karma):
	def __init__(self, ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest):
		super().__init__()
		container = request.body.get('container', None)
		view:dict = request.body.get(container.get('type'))
		title:dict = view.get('title')
		title.update(text=":yin_yang: Karma")
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
class message(karma):
	__doc__ = "Typing `[WORD]++` adds to the karma of [WORD]. `[WORD]--` subtracts from the karma of [WORD]."
	keyword:re = re.compile(f"(<@\w+>|\w+)({plusplus}|{minusminus})")

	def __init__(self, logger:logging.Logger, payload:dict, say:Say):
		super().__init__()
		matches:list = self.keyword.findall(payload.get('text'))
		if matches is not None:
			for match in matches:
				word:str = match[0].lower()
				operator:str = match[1]
				column_name:str = "MINUS" if operator == minusminus else "PLUS"
				select_query:str = select_query(table_name,  where=f"key = '{word}';")
				karma = self.db.cursor.execute(select_query).fetchone()
				if karma is None:
					self.db.cursor.execute(f"INSERT INTO %s(key) VALUES('%s')" % (table_name, word))
					karma = self.db.cursor.execute(select_query).fetchone()
				update_query = f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE key = '{word}'"
				self.db.cursor.execute(update_query)
				self.db.connection.commit()
				try:
					karma = self.db.cursor.execute(select_query).fetchone()
					plusses:int = karma[1]
					minuses:int = karma[2]
					total_score = plusses - minuses
					say(f"*{word}* has {total_score} karma")
				except sqlite3.Error as e:
					logger.error(e)