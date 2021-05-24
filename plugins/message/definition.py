import inspect
import json
import logging
import re
from lib.database import SQLite
from pathlib import Path
from stop_words import get_stop_words

spaces:str = "|".join([' ', '\xa0'])
space_re = f"({spaces})+"
user_re:str = "<@(?P<user_id>[A-Z0-9]+)>"
object_re:str = "(?P<object>\w+)"

plus_operators = ["is",]
minus_operators = ["is not",]
operator_re:str = f"(?P<operator>{'|'.join(minus_operators)}|{'|'.join(plus_operators)})"

definition_re:str = "(?P<definition>\w+)"
keyword:re = re.compile(f"({user_re}|{object_re}){space_re}{operator_re}{space_re}{definition_re}")
table_name = Path(__file__).stem
db = None

def _select(key:str = None):
	logging.debug(inspect.currentframe().f_code.co_name)
	if key is None:
		query:str = f"SELECT KEY, json(DEFS) FROM {table_name}"
		return db.cursor.execute(query, [key]).fetchall()
	else:
		query:str = f"SELECT json(DEFS) FROM {table_name} WHERE key=?"
		values = db.cursor.execute(query, [key]).fetchone()
		if type(values) == type(tuple()):
			return json.loads(values[0])

def _define(key, value):
	logging.debug(inspect.currentframe().f_code.co_name)
	db.cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES(?, json(?))", (key, json.dumps(value)))
	db.connection.commit()

def callback_function(client, context, logger:logging.Logger, next, payload, request, say):
	global db, keyword, table_name, plus_operators, minus_operators
	db = SQLite()
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key text PRIMARY KEY, DEFS json);")
	text = payload.get('text')
	matches = re.finditer(keyword, text)
	for match in matches:
		user_id = match.group('user_id')
		object = match.group('object')
		operator = match.group('operator')
		definition = match.group('definition')
		object = user_id if user_id is not None else object
		if definition not in get_stop_words('english'):
			existing_definitions = _select(object)
			definitions = set(existing_definitions) if existing_definitions is not None else set()
			if operator in plus_operators:
				definitions.add(definition)
			elif definition in definitions:
				definitions.remove(definition)
			_define(object, list(definitions))
			logger.info(f"{object} {operator} {definition}")