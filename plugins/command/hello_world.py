def callback_function(ack, client, request, respond, command):
	ack()
	response_url = request.body.get('response_url', None)
	user_id = command.get('user_id')
	if response_url is not None:
		respond(f"HELLO WORLD (and you, <@{user_id}>)! This code is running from: {__file__}")
	else:
		client.chat_postMessage(
			channel=user_id,
			text=f"Hello <@{user_id}>! :wave:"
		)