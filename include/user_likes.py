from lib.database import SQLite
from lib.slack import whitespace

from pathlib import Path
import logging
import re

space_re = f"({whitespace})+"
self_affirmatives: str = "|".join(["like", "love"])
self_affirmative_re:str = f"({self_affirmatives})"
i_like_re:str = f"(?P<self_reference>I {self_affirmative_re})"

affirmatives: str = "|".join(["likes", "loves"])
affirmative_re:str = f"({affirmatives})"
user_mention_re = "(<@(?P<user_id>[A-Z0-9]+)>)"

user_likes_re = f"{user_mention_re}{space_re}{affirmative_re}"
content_re:str = "(?P<content>.[^.]*)"

keyword:re = re.compile(f"({i_like_re}|{user_likes_re}){space_re}{content_re}")
table_name = Path(__file__).stem

db:SQLite = SQLite()
get_table = db.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
if get_table is None:
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, USER_ID text NOT NULL, LIKES text NOT NULL);")
	db.connection.commit()
db.connection.close()

def db_query(**kwargs):
	global table_name
	columns = kwargs.get('columns', "*")
	order_by = kwargs.get('order_by', "ID")
	order = kwargs.get('order', "ASC")
	where = kwargs.get('where', "")
	return f"SELECT DISTINCT {columns} FROM {table_name} {where} ORDER BY {order_by} {order};"

def blocks(user_id:str):
	blocks:list = []
	db:SQLite = SQLite()
	query = db_query(columns="LIKES", order_by="LIKES", where='WHERE USER_ID=?')
	db_response = db.cursor.execute(query, [user_id]).fetchall()
	if db_response is not None:
		blocks.append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "You like:",
				"emoji": True
			}
		})
		for r in db_response:
			like = r[0]
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": like
				}
			})
	return blocks

def callback_function(logger:logging.Logger, payload, say):
	global table_name
	db:SQLite = SQLite()
	matches:list = keyword.finditer(payload.get('text'))
	if matches is not None:
		for match in matches:
			self_reference = match.group('self_reference')
			user_id = match.group('user_id')
			if self_reference is not None:
				user_id = payload.get('user')
			content = match.group('content')
			db.cursor.execute(f"INSERT INTO {table_name} (USER_ID, LIKES) VALUES(?, ?)", (user_id, content))
			db.connection.commit()

callback_function.__doc__ = "The bot will watch for phrases indicating that users like things, and will keep track of it."