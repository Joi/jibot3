import base64
import logging
import os
from re import S
import sqlite3

from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlite3 import Connection, Cursor, Error

class SQLite():
	connection:Connection = None
	cursor:Cursor = None
	key_file:Path = Path(f"{os.getcwd()}{os.sep}jibot.key")
	db_file:Path = Path(f"{os.getcwd()}{os.sep}sqlite.db")
	cipher:Fernet

	def __init__(self):
		if self.db_file.is_file():
			logging.debug(f"Database file exists... {self.db_file}")
		else:
			logging.debug(f"Database file does not exist... creating {self.db_file}")
			self.db_file.touch()

		try:
			self.connection = sqlite3.connect(self.db_file)
			self.cursor = self.connection.cursor()
			logging.debug(sqlite3.version)
		except Error as e:
			logging.error(e)

		if self.key_file.is_file():
			logging.debug(f"Key file exists... {self.key_file}")
		else:
			logging.debug(f"Key file does not exist... creating {self.key_file}")
			kdf = PBKDF2HMAC(
				algorithm=hashes.SHA256(),
				iterations=100000,
				length=32,
				salt=os.urandom(16),
			)
			passphrase = os.environ.get("JIBOT_CRYPTO_PASS_PHRASE", "").encode('utf-8')
			key = base64.urlsafe_b64encode(kdf.derive(passphrase))
			fernet:Fernet = Fernet(key).generate_key()
			self.key_file.write_bytes(fernet)
		self.cipher = Fernet(open(self.key_file, "rb").read())

	def column_exists(self, table_name:str, column_name:str):
		exists:bool = False
		try:
			self.cursor.execute(f"SELECT {column_name} from {table_name} LIMIT 1;")
			exists = True
		except:
			pass
		return exists

	def table_exists(self, table_name:str):
		exists:bool = False
		try:
			self.cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
			exists = self.cursor.fetchone()[0] == 1
		except:
			pass
		return exists

	def create_table(self, table_name:str, table_details:str):
		self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_details});")

	def delete_table(self, table_name:str):
		self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

	def select_query(self, table_name, **kwargs):
		distinct = "DISTINCT" if kwargs.get('distinct', False) is True else ""
		columns = kwargs.get('columns', "*")
		order_by = f"ORDER BY {kwargs.get('order_by')}" if kwargs.get('order_by') else ""
		order = kwargs.get('order') if  kwargs.get('order') else ""
		where = f"WHERE {kwargs.get('where')}" if kwargs.get('where') else ""
		return f"SELECT {distinct} {columns} FROM {table_name} {where} {order_by} {order};"

	def delete_query(self, table_name:str, where:str):
		return f"DELETE FROM {table_name} {where};"
