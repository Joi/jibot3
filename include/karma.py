from lib.database import SQLite, select_query, get_table, create_table
from pathlib import Path
import logging
import re
import sqlite3

plusplus:str = "\+\+"
minusminus:str = "--"
keyword:re = re.compile(f"(<@\w+>|\w+)({plusplus}|{minusminus})")
table_name:str = Path(__file__).stem

if get_table(table_name) is None:
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

def callback_function(logger:logging.Logger, payload, say):
	global table_name
	matches:list = keyword.findall(payload.get('text'))
	if matches is not None:
		db:SQLite = SQLite()
		for match in matches:
			word:str = match[0].lower()
			operator:str = match[1]
			column_name:str = "MINUS" if operator == minusminus else "PLUS"
			select_query:str = "SELECT * FROM %s WHERE key = '%s';" % (table_name, word)
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