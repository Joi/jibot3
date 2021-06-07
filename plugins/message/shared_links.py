import logging
import re
import sqlite3
from lib.database import SQLite
from pathlib import Path
keyword:re = re.compile("(\w+:\/\/[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\[\]`#|]+)", re.IGNORECASE)
def callback_function(logger:logging.Logger, payload:dict):
	db:SQLite = SQLite()
	table_name:str = Path(__file__).stem
	db.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, URL text NOT NULL);")
	matches:list = keyword.findall(payload.get('text'))
	if matches is not None:
		for url in matches:
			logger.info(f"Saving link: {url}")
			try:
				db.cursor.execute(f"INSERT INTO {table_name} (URL) VALUES(?)", (url,))
				db.connection.commit()
			except sqlite3.Error as e:
				logger.error(e)