from wikipedia import WikipediaPage, WikipediaException
import wikipedia
import logging

def get_url(search_term:str):
	try:
		wiki_page:WikipediaPage = wikipedia.page(search_term)
		return wiki_page.url
	except WikipediaException as e:
		logging.error(e)
		return None