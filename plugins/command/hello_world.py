import os
from lib.slack import slack_bot_slash_command as bot_slash_command

def callback_function(ack, client, request, respond, command):
	ack()
	response_url = request.body.get('response_url', None)
	user_id = command.get('user_id')
	relative_path = os.path.relpath(__file__, os.getcwd())
	if response_url is not None:
		respond(f"HELLO WORLD (and you, <@{user_id}>)! This code is running from: {relative_path}")
	else:
		client.chat_postMessage(
			channel=user_id,
			text=f"Hello <@{user_id}>! :wave:"
		)
callback_function.__doc__ = f"When a user types `/{bot_slash_command} hello world` the bot says hello back."