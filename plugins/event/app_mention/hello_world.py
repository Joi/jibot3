import os
def callback_function(event, say):
	user = event['user']
	relative_path = os.path.relpath(__file__, os.getcwd())
	say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {relative_path}")
callback_function.__doc__ = f"`hello_world` the bot says hello back."