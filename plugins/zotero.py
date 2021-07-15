import include.zotero as Zotero

from slack_bolt import Ack, BoltRequest, BoltResponse
from slack_bolt.context import BoltContext
from slack_sdk.models.views import View
from slack_sdk.web import WebClient
import logging


class view(Zotero.Zotero):
    def __init__(self, ack:Ack, client:WebClient, context:BoltContext, logger:logging.Logger, request:BoltRequest, view:View):
        super(context.get('user_id'))
        state:dict = view.get('state')
        form_fields:dict = state['values']
        sql_fields:dict = { 'user_id': context.get('user_id') }
        for i in form_fields:
            form_field:dict = form_fields[i]
            for t in form_field:
                field_name:str = t
                field = form_field[t]
                field_type = field.get('type')
                field_value:dict = field.get('value')
                if field_type == 'static_select':
                    field_value = field.get('selected_option').get('value')

                if field_value is None and hasattr(self, field_name):
                    field_value = getattr(self, field_name)

                if field_name == 'zotero_api_key':
                    field_value =  self.db.cipher.encrypt(field_value.encode('utf-8'))

                sql_fields[field_name] =  field_value

        placeholders: list = []
        for i in range (0, len(sql_fields)):
            placeholders.append("?")

        placeholder:str = ','.join(placeholders)
        field_names:str = ', '.join(sql_fields.keys())
        insert_query = f"INSERT OR REPLACE INTO {self.table_name} ({field_names}) VALUES({placeholder})"
        self.db.cursor.execute(insert_query, list(sql_fields.values()))
        self.db.connection.commit()
        ack()

class action(Zotero.Zotero):
    zotero = None
    def __init__(self, ack:Ack, client:WebClient, context:BoltContext, logger:logging.Logger, payload:dict, request:BoltRequest):
        super(context.get('user_id'))
        container = request.body.get('container', None)
        view:dict = request.body.get(container.get('type'))
        title:dict = view.get('title')
        title.update(text="Zotero Integration")
        close_button = view.get('close')
        close_button.update(text="Go Back")
        blocks:list = list()
        intro = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "The area is used to configure your slack / zotero integration."
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
                "placeholder": {
                    "type": "plain_text",
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

        library_type = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Library Type",
                    "emoji": True
                },
                "options": library_type_options,
                "action_id": "zotero_library_type"
            },
            "label": {
                "type": "plain_text",
                "text": ":books: Library Type",
                "emoji": True
            }
        }

        if self.zotero_library_type is not None:
            current_library_type = next((x for x in library_type_options if x.get('value') == self.zotero_library_type), library_type_options[0])
            library_type['element']["initial_option"] = current_library_type

        if self.zotero_library_id is not None:
            library_id['element']["initial_value"] = self.zotero_library_id

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