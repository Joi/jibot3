import base64
import logging
import os
import sqlite3
from sqlite3 import Connection, Cursor, Error
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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

def column_exists(table_name:str, column_name:str):
	db:SQLite = SQLite()
	exists:bool = False
	try:
		db_response = db.cursor.execute(f"SELECT {column_name} from {table_name} LIMIT 1;")
		exists = True
	except:
		pass
	return exists

def table_exists(table_name:str):
	db:SQLite = SQLite()
	exists:bool = False
	try:
		db_response:Cursor = db.cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
		exists = db.cursor.fetchone()[0] == 1
	except:
		pass
	return exists

def create_table(table_name:str, table_details:str):
	db:SQLite = SQLite()
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_details});")

def delete_table(table_name:str):
	db:SQLite = SQLite()
	db.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

def _cipher():
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		iterations=100000,
		length=32,
		salt=os.urandom(16),
	)
	passphrase = os.environ.get("JIBOT_CRYPTO_PASS_PHRASE", "").encode('UTF-8')
	key = base64.urlsafe_b64encode(kdf.derive(passphrase))
	fernet:Fernet = Fernet(key)
	return fernet

cipher = _cipher()

def select_query(table_name, **kwargs):
	distinct = "DISTINCT" if kwargs.get('distinct', False) is True else ""
	columns = kwargs.get('columns', "*")

	order_by = f"ORDER BY {kwargs.get('order_by')}" if kwargs.get('order_by') else ""
	order = kwargs.get('order') if  kwargs.get('order') else ""
	where = f"WHERE {kwargs.get('where')}" if kwargs.get('where') else ""
	return f"SELECT {distinct} {columns} FROM {table_name} {where} {order_by} {order};"

def delete_query(table_name:str, where:str):
	return f"DELETE FROM {table_name} {where};"
