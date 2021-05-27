import logging
from pathlib import Path
import re
import sqlite3
from typing import List
from lib.database import SQLite

plusplus:str = "\+\+"
minusminus:str = "--"
keyword:re = re.compile(f"(\w+)({plusplus}|{minusminus})")
def callback_function(client, context, logger:logging.Logger, next, payload, request, say):
	db:SQLite = SQLite()
	table_name:str = Path(__file__).stem
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key text PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0);")
	matches:List = keyword.findall(payload.get('text'))
	if matches is not None:
		for match in matches:
			word:str = match[0]
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