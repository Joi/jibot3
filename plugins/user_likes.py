from lib.database import SQLite
from lib.slack import whitespace

from pathlib import Path
import logging
import re
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say


table_name = Path(__file__).stem
table_params = "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, USER_ID text NOT NULL, LIKES text NOT NULL, UNIQUE(USER_ID, LIKES)"
SQLite().create_table(table_name, table_params)

class user_likes:
	db:SQLite
	select_query:str

	def __init__(self):
		self.db = SQLite()
		self.select_query = self.db.select_query(table_name, columns="LIKES", order_by="LIKES", distinct=True, where='USER_ID=?')

	def blocks(self, user_id:str):
		blocks:list = []
		db_response = self.db.cursor.execute(self.select_query, [user_id]).fetchall()
		if db_response is not None:
			blocks.append({
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": ":+1: You like:",
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

class message(user_likes):
	space_re = f"({whitespace})+"
	self_affirmatives: str = "|".join(["like", "love"])
	self_affirmative_re:str = f"({self_affirmatives})"
	i_like_re:str = f"(?P<self_reference>I{space_re}{self_affirmative_re})"
	affirmatives: str = "|".join(["likes", "loves"])
	affirmative_re:str = f"({affirmatives})"
	user_mention_re = "(<@(?P<user_id>[A-Z0-9]+)>)"
	user_likes_re = f"{user_mention_re}{space_re}{affirmative_re}"
	content_re:str = "(?P<content>.[^.]*)"
	keyword:re = re.compile(f"({i_like_re}|{user_likes_re}){space_re}{content_re}", re.IGNORECASE)

	def __init__(self, logger:logging.Logger, payload:dict, say:Say):
		super().__init__()
		matches:list = self.keyword.finditer(payload.get('text'))
		if matches is not None:
			for match in matches:
				self_reference = match.group('self_reference')
				user_id = match.group('user_id')
				if self_reference is not None:
					user_id = payload.get('user')
				content = match.group('content')
				self.db.cursor.execute(f"INSERT OR IGNORE INTO {table_name} (USER_ID, LIKES) VALUES(?, ?)", (user_id, content))
				self.db.connection.commit()