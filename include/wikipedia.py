from wikipedia import WikipediaPage, WikipediaException
import wikipedia
from lib.slack import logger

def get_url(search_term:str):
	try:
		wiki_page:WikipediaPage = wikipedia.page(search_term)
		return wiki_page.url
	except WikipediaException as e:
		logger.error(e)
		return None
