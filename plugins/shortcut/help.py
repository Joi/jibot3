from slack_sdk.web import WebClient
def callback_function(ack, client:WebClient, logger, shortcut):
	ack()
	logger.info(shortcut)
	view = client.views_open(
        trigger_id=shortcut["trigger_id"],
		view={
			"type": "modal",
            "title": {"type": "plain_text", "text": "Help"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": []
        }
    )