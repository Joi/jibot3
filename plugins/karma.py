from lib.database import SQLite, select_query, table_exists, create_table
from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_sdk.web import WebClient
import logging
import re
import sqlite3

table_name:str = Path(__file__).stem
plusplus:str = "\+\+"
minusminus:str = "--"

if not table_exists(table_name):
	create_table(table_name, "key text PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0")

def blocks():
	global table_name
	blocks:list = []
	db:SQLite = SQLite()
	karma_karma_karma_karma_karma_queryaaaaa:str = select_query(table_name)
	karma = db.cursor.execute(karma_karma_karma_karma_karma_queryaaaaa).fetchall()
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

class action:
	def __init__(self, ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest):
		container = request.body.get('container', None)
		view:dict = request.body.get(container.get('type'))
		title:dict = view.get('title')
		title.update(text=":yin_yang: Karma")
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
	keyword:re = re.compile(f"(<@\w+>|\w+)({plusplus}|{minusminus})")
	__doc__ = "Typing `[WORD]++` adds to the karma of [WORD]. `[WORD]--` subtracts from the karma of [WORD]."
	def __init__(self, logger:logging.Logger, payload:dict, say:Say):
		matches:list = self.keyword.findall(payload.get('text'))
		if matches is not None:
			db:SQLite = SQLite()
			for match in matches:
				word:str = match[0].lower()
				operator:str = match[1]
				column_name:str = "MINUS" if operator == minusminus else "PLUS"
				select_query:str = select_query(table_name,  where=f"key = '{word}';")
				karma = db.cursor.execute(select_query).fetchone()
				if karma is None:
					db.cursor.execute(f"INSERT INTO %s(key) VALUES('%s')" % (table_name, word))
					karma = db.cursor.execute(select_query).fetchone()
				update_query = f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE key = '{word}'"
				db.cursor.execute(update_query)
				db.connection.commit()
				try:
					karma = db.cursor.execute(select_query).fetchone()
					plusses:int = karma[1]
					minuses:int = karma[2]
					total_score = plusses - minuses
					say(f"*{word}* has {total_score} karma")
				except sqlite3.Error as e:
					logger.error(e)