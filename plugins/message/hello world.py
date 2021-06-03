import os
from pathlib import Path
def callback_function(message, say):
	user = message['user']
	relative_path = os.path.relpath(__file__, os.getcwd())
	say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {relative_path}")
callback_function.__doc__ = f"When the bot sees a user say `{Path(__file__).stem}` the bot says hello back."