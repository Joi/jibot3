from slack_bolt import Say
import os

class message:
	keyword:str = "hello world"
	__doc__ = f"When the bot sees someone say {keyword}, the bot says hello back."
	def __init__(self, payload:dict, say:Say):
		user = payload['user']
		say(f"HELLO WORLD (and you, <@{user}>)!")