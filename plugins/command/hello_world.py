def callback_function(client, command, context, logger, next, payload, request, response, respond, say):
	user = payload['user_id']
	say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {__file__}")