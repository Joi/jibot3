import logging
from slack_bolt.context.context import BoltContext
from lib.database import SQLite, select_query

from pathlib import Path
from pyzotero import zotero as PyZotero
from slack_bolt import Ack, BoltRequest, BoltResponse, Respond

class Zotero:
    table_name:str = Path(__file__).stem
    library = None

    def __init__(self, user_id:str = None):
        print(f"INIT ZOTERO {user_id}")
        if user_id is not None:
            config = self.config(user_id)
            self.library = PyZotero.Zotero(config.get('zotero_library_id'), config.get('zotero_library_type'), config.get('zotero_api_key'))

    def config(self, user_id:str):
        db:SQLite = SQLite()
        select = select_query(self.table_name, where=f"user_id = '{user_id}'")
        config = db.cursor.execute(select).fetchone()
        if config:
            return {
                'user_id' : config[0],
                'zotero_library_type' : config[1],
                'zotero_library_id' : config[2],
                'zotero_api_key' : config[3],
            }
    def read(self, ack:Ack, context:BoltContext, logger:logging.Logger, payload:dict, request: BoltRequest, respond:Respond):
        self.__init__(context.get('bot_user_id'))
        print("READ ZOTERO")
