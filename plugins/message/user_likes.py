import logging
from pathlib import Path
import re
from lib.database import SQLite
from lib.slack import whitespace

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
def callback_function(logger:logging.Logger, payload, say):
	db:SQLite = SQLite()
	table_name:str = Path(__file__).stem
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, USER_ID text NOT NULL, LIKES text NOT NULL);")
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