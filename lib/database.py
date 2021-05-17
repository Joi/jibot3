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