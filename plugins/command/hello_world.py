def callback_function(**args):
	ack = args['ack']
	payload = args['payload']
	say = args['say']
	user = payload['user_id']
	ack()
	say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {__file__}")