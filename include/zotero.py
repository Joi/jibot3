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
            self.user_id = user_id
            select = self.db.select_query(table_name, where=f"user_id = '{self.user_id}'")
            config = self.db.cursor.execute(select).fetchone()
            if config is not None:
                self.zotero_library_type = config[1]
                self.zotero_library_id = config[2]
                self.zotero_api_key = self.db.cipher.decrypt(config[3]).decode('utf-8')
                self.library = PyZotero.Zotero(self.zotero_library_id, self.zotero_library_type, self.zotero_api_key)

    def block(self, zotero_item):
        response_text:str = zotero_item
        if type(zotero_item) != type(""):
            zotero_data = zotero_item.get('data')
            response_text = f"<{zotero_data.get('url')}|{zotero_data.get('title')}>"

        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": response_text
            },
        }
    def blocks(self, zotero_items):
        blocks:list = []
        for zotero_item in zotero_items:
            blocks.append(self.block(zotero_item))
        return blocks

    def no_integration(self):
        return [f":warning:  <@{self.user_id}> You have not set up a zotero integration."]

    def read(self, search_term:str = None):
        if self.library is None:
            return self.no_integration()

        if not search_term:
            return self.library.items()
        else:
            return self.library.items(q=search_term)
