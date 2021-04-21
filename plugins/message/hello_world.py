keyword="hello world"
def callback_function(message, say):
	user = message['user']
	say(f"HELLO WORLD (and you, <@{user}>)! This code is running from: {__file__}")