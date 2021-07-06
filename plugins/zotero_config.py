from lib.database import SQLite, select_query, table_exists, create_table, delete_table, column_exists, cipher

from pathlib import Path
from slack_bolt import Ack, BoltRequest, BoltResponse
from slack_bolt.context import BoltContext
from slack_sdk.models.views import View
from slack_sdk.web import WebClient
import logging

table_name:str = Path(__file__).stem
if not table_exists(table_name):
    create_table(table_name, "user_id text PRIMARY KEY UNIQUE, zotero_library_type text NOT NULL, zotero_library_id text NOT NULL, zotero_api_key BLOB NOT NULL")

def _get_config(user_id):
        db:SQLite = SQLite()
        select = select_query(table_name, where=f"user_id = '{user_id}'")
        config = db.cursor.execute(select).fetchone()
        return {
            'user_id' : config[0],
            'zotero_library_type' : config[1],
            'zotero_library_id' : config[2],
            'zotero_api_key' : config[3],
        }

class view:
    keyword:str = table_name
    def __init__(self, ack:Ack, client:WebClient, context:BoltContext, logger:logging.Logger, request:BoltRequest, view:View):
        bot_config = _get_config(context.get('bot_user_id'))
        state:dict = view.get('state')
        form_fields:dict = state['values']
        sql_fields:dict = { 'user_id': context.get('bot_user_id') }

        for i in form_fields:
            form_field:dict = form_fields[i]
            for t in form_field:
                field_name:str = t
                field = form_field[t]
                field_type = field.get('type')
                field_value:dict = field.get('value')
                if field_type == 'static_select':
                    field_value = field.get('selected_option').get('value')

                if field_value is None:
                   field_value = bot_config.get(field_name)

                sql_fields[field_name] =  field_value
                if field_name == 'zotero_api_key':
                    sql_fields[field_name] =  cipher.encrypt(field_value.encode('UTF-8'))

        placeholders: list = []
        for i in range (0, len(sql_fields)): placeholders.append("?")

        db:SQLite = SQLite()
        placeholder:str = ','.join(placeholders)
        field_names:str = ', '.join(sql_fields.keys())
        insert_query = f"INSERT OR REPLACE INTO {table_name} ({field_names}) VALUES({placeholder})"
        print(insert_query)
        db.cursor.execute(insert_query, list(sql_fields.values()))
        db.connection.commit()
        ack()

class action:
    keyword:str = table_name
    def __init__(self, ack:Ack, client:WebClient, context:BoltContext, logger:logging.Logger, payload:dict, request:BoltRequest):

        bot_config = _get_config(context.get('bot_user_id'))

        container = request.body.get('container', None)
        view:dict = request.body.get(container.get('type'))
        title:dict = view.get('title')
        title.update(text="Slack-Wide Zotero")
        close_button = view.get('close')
        close_button.update(text="Go Back")
        blocks:list = list()
        db:SQLite = SQLite()
        select = select_query(table_name, where=f"user_id = '{context.get('bot_user_id')}'")

        intro = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "The area is used to configur a a slack-wide zotero integration."
            }
        }
        link = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You can create and configure Zotero API settings at <https://www.zotero.org/settings/keys|Zotero API Settings>"
			}
		}
        library_id = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "zotero_library_id",
                "initial_value": bot_config.get('zotero_library_id', ""),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Helpful placeholder text goes here",
                    "emoji": True
                },

            },
            "label": {
                "type": "plain_text",
                "text": ":id: Library ID",
                "emoji": True
            }
        }
        library_type_options = [
            {
                "text": {
                    "type": "plain_text",
                    "text": ":bust_in_silhouette: User",
                    "emoji": True
                },
                "value": "user",
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": ":busts_in_silhouette: Group",
                    "emoji": True
                },
                "value": "group",
            }
        ]

        current_library_type = next((x for x in library_type_options if x.get('value') == bot_config.get('type')), library_type_options[0])

        library_type = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Library Type",
                    "emoji": True
                },
                "initial_option": current_library_type,
                "options": library_type_options,
                "action_id": "zotero_library_type"
            },
            "label": {
                "type": "plain_text",
                "text": ":books: Library Type",
                "emoji": True
            }
        }
        api_key = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "zotero_api_key",
                "placeholder": {
                    "type": "plain_text",
                    "text": "HIDDEN FOR PRIVACY",
                    "emoji": True
                },
            },
            "label": {
                "type": "plain_text",
                "text": ":key: Api Key",
                "emoji": True
            },
            "optional": True
        }
        blocks.extend([
            intro,
            link,
            library_type,
            library_id,
            api_key
        ])
        client.views_push(
            trigger_id=request.body.get('trigger_id'),
            view={
                "type": view.get('type'),
                "title": title,
                "close": close_button,
                "callback_id": self.keyword,
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True,
                },
                "blocks": blocks
            }
        )
        ack()