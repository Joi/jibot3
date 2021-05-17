import logging
from pathlib import Path
import re
import sqlite3
from lib.database import SQLite

plusplus:str = "\+\+"
minusminus:str = "--"
keyword:re = re.compile(f"(\w+)({plusplus}|{minusminus})")
def callback_function(client, context, logger:logging.Logger, next, payload, request, say):
	db = SQLite()
	table_name = Path(__file__).stem
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key int PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0);")
	matches = keyword.findall(payload.get('text'))
	if matches is not None:
		for match in matches:
			word = match[0]
			operator = match[1]
			column_name = "MINUS" if operator == minusminus else "PLUS"
			select_query = f"SELECT * FROM {table_name} WHERE key = '{word}';"
			eliteness = db.cursor.execute(select_query).fetchone()
			if eliteness is None:
				db.cursor.execute(f"INSERT INTO {table_name}(key) VALUES('{word}')")
				eliteness = db.cursor.execute(select_query).fetchone()
			update_query = f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE key = '{word}'"
			db.cursor.execute(update_query)
			db.connection.commit()
			try:
				eliteness = db.cursor.execute(select_query).fetchone()
				plusses:int = eliteness[1]
				minuses:int = eliteness[2]
				total_score = plusses - minuses
				say(f"Eliteness score updated for *'{word}'*: {total_score} `(+{plusses} -{minuses})`")
			except sqlite3.Error as e:
				logger.error(e)