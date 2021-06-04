import json
import logging
from slack_bolt import Ack, BoltRequest
from slack_sdk.web import WebClient
from lib.database import SQLite

def callback_function(ack:Ack, client:WebClient, logger:logging.Logger, request:BoltRequest, view:dict):
	print(__file__)
	print(__file__)
	print(__file__)
	ack()
	# container = request.body.get('container', None)
	# blocks:list = []
	# db:SQLite = SQLite()
	# karma_karma_karma_karma_karma_queryaaaaa:str = "SELECT * FROM karma ORDER BY key ASC;"
	# # container = request.body.get('container')
	# # view:dict = request.body.get(container.get('type'))
