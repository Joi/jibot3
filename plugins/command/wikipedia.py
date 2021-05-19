import wikipedia
from pathlib import Path
from wikipedia import WikipediaPage, WikipediaException

def callback_function(client, command, context, logger, next, payload, request, response, respond, say):
	keyword = Path(__file__).stem
	text = payload.get('text', None)
	message:list = []
	if text is not None:
		search_term = text.replace(keyword, "").strip()
		try:
			wiki_page:WikipediaPage = wikipedia.page(search_term)
			message.append(wiki_page.url)
		except WikipediaException as e:
			message.append(str(e))
	say(text=" ".join(message))