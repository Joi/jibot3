from lib.database import SQLite, select_query, table_exists, create_table, delete_table, column_exists

import inspect
import json
import logging
import re

from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from stop_words import get_stop_words



def _select(key:str = None):
	logging.debug(inspect.currentframe().f_code.co_name)
	db:SQLite = SQLite()
	db_response = None
	if key is None:
		query:str = select_query(table_name, columns="OBJECT, ATTRIBUTE")
		db_response =  db.cursor.execute(query, [key]).fetchall()
	else:
		query:str = select_query(table_name, columns="OBJECT, ATTRIBUTE", where="WHERE OBJECT=?")
		db.cursor.execute(query).fetchall()
	# if type(values) == type(tuple()):
	# 	db_response =  json.loads(values[0])
	return db_response

def _define(object, attribute):
	logging.debug(inspect.currentframe().f_code.co_name)
	db:SQLite = SQLite()
	db.cursor.execute(f"INSERT OR IGNORE INTO {table_name} (OBJECT, ATTRIBUTE) VALUES(?, ?)", (object, attribute))
	db.connection.commit()

def _undefine(object, attribute):
	logging.debug(inspect.currentframe().f_code.co_name)
	db:SQLite = SQLite()
	db.cursor.execute(f"DELETE FROM {table_name} WHERE OBJECT=? AND ATTRIBUTE=?", (object, attribute))
	db.connection.commit()

table_schema:str = "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, OBJECT text NOT NULL, ATTRIBUTE text NOT NULL, UNIQUE(OBJECT, ATTRIBUTE)"
table_name = Path(__file__).stem
if not table_exists(table_name):
	create_table(table_name, table_schema)
else:
	if column_exists(table_name, "DEFS"):
		data = _select()
		tmp_table_name = f"__migrate_{table_name}"
		db:SQLite = SQLite()
		db.cursor.execute(f"ALTER TABLE {table_name} RENAME TO {tmp_table_name};")
		create_table(table_name, table_schema)
		if data is not None:
			for d in data:
				o:str = d[0]
				atts:list = json.loads(d[1])
				for att in atts:
					_define(o, att)
		if table_exists(table_name) and table_exists(tmp_table_name):
			delete_table(tmp_table_name)

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

class message:
	spaces:str = "|".join([' ', '\xa0'])
	space_re = f"({spaces})+"
	user_re:str = "<@(?P<user_id>[A-Z0-9]+)>"
	object_re:str = "(?P<object>\w+)"
	plus_operators = ["is the", "is", "are"]
	minus_operators = ["is not the", "is not", "isn't", "are not", "aren't"]
	operator_re:str = f"(?P<operator>{'|'.join(minus_operators)}|{'|'.join(plus_operators)})"
	definition_re:str = "(?P<definition>\w+)"
	keyword:re = re.compile(f"({user_re}|{object_re}){space_re}{operator_re}{space_re}{definition_re}")

	def __init__(self, logger:logging.Logger, payload:dict, request:BoltRequest, say:Say):
		matches = re.finditer(self.keyword, payload.get('text'))
		for match in matches:
			user_id = match.group('user_id')
			object = match.group('object').lower()
			operator = match.group('operator')
			definition = match.group('definition')
			object = user_id if user_id is not None else object
			logger.info(f"{object} {operator} {definition}")

			if definition not in get_stop_words('english'):
				if operator in self.plus_operators:
					_define(object, definition)
				else:
					_undefine(object, definition)
