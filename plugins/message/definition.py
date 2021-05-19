import logging
from pathlib import Path
import re
import sqlite3
from lib.database import SQLite

spaces:str = "|".join([' ', '\xa0'])
space_re = f"({spaces})+"

user_re:str = "<@(?P<user_id>[A-Z0-9]+)>"
thing_re:str = "(?P<thing>\w+)"
operator_re:str = "(?P<operator>is not|is)"
att_re:str = "(?P<attribute>\w+)"
keyword:re = re.compile(f"({user_re}|{thing_re}){space_re}{operator_re}{space_re}{att_re}")

def callback_function(client, context, logger:logging.Logger, next, payload, request, say):
	global keyword
	# db = SQLite()
	# table_name = Path(__file__).stem
	# db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key text PRIMARY KEY, PLUS int DEFAULT 0, MINUS int DEFAULT 0);")
	text = payload.get('text')
	matches = re.finditer(keyword, text)
	for match in matches:
		user_id = match.group('user_id')
		thing = match.group('thing')
		operator = match.group('operator')
		attribute = match.group('attribute')
		object = user_id if user_id is not None else thing
		logger.info(f"{object} {operator} {attribute}")