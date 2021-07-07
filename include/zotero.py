import logging
from slack_bolt.context.context import BoltContext
from lib.database import SQLite

from pathlib import Path
from pyzotero import zotero as PyZotero
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond

table_name:str = Path(__file__).stem
table_params:str = "user_id text PRIMARY KEY UNIQUE, zotero_library_type text NOT NULL, zotero_library_id text NOT NULL, zotero_api_key BLOB NOT NULL"
SQLite().create_table(table_name, table_params)

class Zotero:
    db:SQLite
    keyword:str = table_name
    table_name:str = table_name
    zotero_library_id:str = None
    zotero_library_type:str = None
    zotero_api_key:bytes = None
    library:PyZotero.Zotero = None

    def __init__(self, user_id:str = None):
        self.db = SQLite()
        if user_id is not None:
            select = self.db.select_query(table_name, where=f"user_id = '{user_id}'")
            config = self.db.cursor.execute(select).fetchone()
            if config is not None:
                self.user_id = config[0]
                self.zotero_library_type = config[1]
                self.zotero_library_id = config[2]
                self.zotero_api_key = self.db.cipher.decrypt(config[3]).decode('utf-8')
                self.library = PyZotero.Zotero(self.zotero_library_id, self.zotero_library_type, self.zotero_api_key)

    def read(self, ack:Ack, context:BoltContext, logger:logging.Logger, payload:dict, request: BoltRequest, respond:Respond):
        items = self.library.items()
        print(items)
