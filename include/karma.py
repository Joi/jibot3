from lib.database import SQLite, select_query, table_exists, create_table
from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
import logging
import re
import sqlite3


table_name:str = Path(__file__).stem
plusplus:str = "\+\+"
minusminus:str = "--"

if not table_exists(table_name):
	create_table(table_name, "key text PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0")

class message:
	keyword:re = re.compile(f"(<@\w+>|\w+)({plusplus}|{minusminus})")
	def __init__(self, logger:logging.Logger, payload:dict, say:Say):
		matches:list = self.keyword.findall(payload.get('text'))
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