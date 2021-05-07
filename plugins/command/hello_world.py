def callback_function(ack, client, command, logger, context, next, options, payload, request, response, respond, say):
	return say(f"HELLO WORLD! This command is running from: {__file__}")