import wikipedia
from pathlib import Path
from wikipedia import WikipediaPage, WikipediaException

def callback_function(**args):
	keyword = Path(__file__).stem
	ack = args['ack']
	payload = args['payload']
	say = args['say']
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
	ack()