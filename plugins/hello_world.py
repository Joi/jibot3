from slack_bolt import Say
import os
from pathlib import Path

class message:
	keyword:str = "hello world"
	def __init__(self, payload:dict, say:Say):
		user = payload['user']
		relative_path = os.path.relpath(__file__, os.getcwd())
		say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {relative_path}")
	__doc__ = f"When the bot sees a user say `{Path(__file__).stem}` the bot says hello back."