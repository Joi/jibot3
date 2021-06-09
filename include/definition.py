from lib.database import SQLite, select_query, get_table, create_table
import inspect
import json
import logging
import re
from pathlib import Path
from stop_words import get_stop_words

spaces:str = "|".join([' ', '\xa0'])
space_re = f"({spaces})+"
user_re:str = "<@(?P<user_id>[A-Z0-9]+)>"
object_re:str = "(?P<object>\w+)"

plus_operators = ["is the", "is", "are"]
minus_operators = ["is not the", "is not", "isn't", "are not", "aren't"]
operator_re:str = f"(?P<operator>{'|'.join(minus_operators)}|{'|'.join(plus_operators)})"

definition_re:str = "(?P<definition>\w+)"
keyword:re = re.compile(f"({user_re}|{object_re}){space_re}{operator_re}{space_re}{definition_re}")
table_name = Path(__file__).stem

if get_table(table_name) is None:
	create_table(table_name, "key text PRIMARY KEY, DEFS json")

def _select(key:str = None):
	logging.debug(inspect.currentframe().f_code.co_name)
	db:SQLite = SQLite()
	db_response = None
	if key is None:
		# query:str = f"SELECT KEY, json(DEFS) FROM {table_name}"
		query:str = select_query(table_name, columns="KEY, json(DEFS)")
		db_response =  db.cursor.execute(query, [key]).fetchall()
	else:
		query:str = select_query(table_name, columns="KEY, json(DEFS)", where="WHERE key=?")
		values = db.cursor.execute(query, [key]).fetchone()
		if type(values) == type(tuple()):
			db_response =  json.loads(values[0])
	return db_response

def _define(key, value):
	logging.debug(inspect.currentframe().f_code.co_name)
	db:SQLite = SQLite()
	db.cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES(?, json(?))", (key, json.dumps(value)))
	db.connection.commit()

def blocks():
	blocks:list = []
	db:SQLite = SQLite()
	definition_query:str = "SELECT * FROM definition ORDER BY key ASC;"
	definition = db.cursor.execute(definition_query).fetchall()
	if definition is not None:
		for d in definition:
			thing:str = d[0]
			definitions = json.loads(d[1])
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"*{thing}:* {', '.join(definitions)}"
				}
			})
	return(blocks)

def callback_function(logger:logging.Logger, payload, request, say):
	global keyword, table_name, plus_operators, minus_operators
	text = payload.get('text')
	matches = re.finditer(keyword, text)
	for match in matches:
		user_id = match.group('user_id')
		object = match.group('object').lower()
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