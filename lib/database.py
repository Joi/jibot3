import logging
import sqlite3
from sqlite3 import Connection, Cursor, Error

class SQLite():
	connection:Connection = None
	cursor:Cursor = None
	db_file: str = 'sqlite.db'
	def __init__(self, db_file:str = None):
		if db_file is not None:
			self.db_file = db_file
		try:
			self.connection = sqlite3.connect(self.db_file)
			self.cursor = self.connection.cursor()
			logging.debug(sqlite3.version)
		except Error as e:
			logging.error(e)

def get_table(table_name):
	db:SQLite = SQLite()
	return db.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

def create_table(table_name:str, table_details:str):
	db:SQLite = SQLite()
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_details});")

def db_query(table_name, **kwargs):
	distinct = "DISTINCT" if kwargs.get('distinct', False) is True else ""
	columns = kwargs.get('columns', "*")
	order_by = kwargs.get('order_by', "key")
	order = kwargs.get('order', "ASC")
	where = kwargs.get('where', "")
	return f"SELECT {distinct} {columns} FROM {table_name} {where} ORDER BY {order_by} {order};"