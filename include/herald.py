import json
import os
from plugins.user_likes import user_likes
from plugins.user_dislikes import user_dislikes

from slack_bolt import Ack, BoltRequest, BoltResponse, Respond, Say
from slack_bolt.context import BoltContext
from slack_sdk.web import WebClient, slack_response

class herald:
    user_id:str
    def __init__(self, ack: Ack, client:WebClient, context:BoltContext, payload:dict, request:BoltRequest, respond:Respond, say:Say):
        ack()
        self.user_id = context.get('user_id')
        if payload.get('text') is not None:
            who_to_herald, sep, payload_text = payload.get('text').partition(" ")
            if who_to_herald != "me":
                user_token = os.environ.get("JIBOT_SLACK_USER_TOKEN", None)
                user_response:slack_response = client.users_identity(token=user_token, name=who_to_herald)
                if user_response.get('ok'):
                    self.user_id = user_response.get('user').get('id')

            if respond.response_url is None:
                say(blocks=self.blocks())
            else:
               respond(blocks=self.blocks())

    def blocks(self):
        blocks:list  = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Huzzah to <@{self.user_id}>!"
            }
        }]
        blocks.extend(user_likes().blocks(self.user_id))
        blocks.extend(user_dislikes().blocks(self.user_id))
        return blocks