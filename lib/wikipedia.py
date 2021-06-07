import wikipedia
from lib.slack import get_bot_mention_text
from pathlib import Path
from slack_bolt.context.respond import Respond
from wikipedia import WikipediaPage, WikipediaException
def callback_function(ack, context, payload, say, respond:Respond):
	keyword = Path(__file__).stem
	text = get_bot_mention_text(context.get('bot_user_id'), payload.get('text'))
	message:list = []
	if text is not None:
		search_term = text.replace(keyword, "").strip()
		try:
			wiki_page:WikipediaPage = wikipedia.page(search_term)
			message.append(wiki_page.url)
		except WikipediaException as e:
			message.append(str(e))
	if respond.response_url is not None:
		respond(text=" ".join(message))
	else:
		say(text=" ".join(message))
	ack()
callback_function.__doc__ = f"Wikipedia lookup"