import hashlib
import json
import matplotlib.pyplot as plt
import nltk
import os
import sqlite3
import sys
import urllib.request

from bs4 import BeautifulSoup

stopwords = nltk.corpus.stopwords.words('english')
tokenizer = nltk.RegexpTokenizer(r"\w+")

def plot(args):
	if args.get("col") and args.get("table") and args.get("id") and args.get("dbpath"):
		dbpath = args.get("dbpath")
		if (dbpath is None):
			bpath = "../db/database.sqlite"
		conn = sqlite3.connect(dbpath)
		cur = conn.cursor()
		cur.execute("SELECT %s FROM %s WHERE id=%s" % (args["col"], args["table"], args["id"]))
		text = cur.fetchone()[0]

	elif args.get("url"):
		fp = urllib.request.urlopen(args["url"])
		soup = BeautifulSoup(fp.read().decode("utf8"), 'html.parser')
		text = soup.get_text()
		fp.close()

	elif args.get("text"):
		text = args.get("text")

	words = []
	pwd = os.path.dirname(os.path.realpath(__file__))
	checksum = hashlib.md5(text.encode('utf-8')).hexdigest()
	filename = f"{checksum}.png"
	outpath = f"{pwd}/images/{filename}"
	for w in tokenizer.tokenize(text):
		word = w.lower()
		if  word not in stopwords:
			words.append(word)
	plt.ion()
	fd = nltk.probability.FreqDist(words)
	fd.plot(10, cumulative=False)
	plt.savefig(outpath)
	plt.ioff()
	print(outpath);
	sys.stdout.flush()

def main():
	if (sys.argv and sys.argv[1]):
		command = sys.argv[1]
	if (sys.argv and sys.argv[2]):
		args = json.loads(sys.argv[2])
	if (command and args):
		eval(f"{command}(args)")

if __name__ == '__main__':
	main()