import nltk
import requests
import hashlib
import sys
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from PIL import Image
import io

stopwords = nltk.corpus.stopwords.words('english')
tokenizer = nltk.RegexpTokenizer(r"\w+")

def freq_dist(text):
    words = []
    checksum = hashlib.md5(text.encode('utf-8')).hexdigest()
    filename = f"{checksum}.png"
    for w in tokenizer.tokenize(text):
        word = w.lower()
        if  word not in stopwords:
            words.append(word)
    plt.ion()
    fd = nltk.probability.FreqDist(words)
    fd.plot(10, cumulative=False)
    plt.savefig(filename)
    plt.ioff()
    # im = Image.open(filename)
    # fp = io.BytesIO()
    # im.save(fp, format=im.format)
    # print(fp.getvalue())
    print(filename);
    sys.stdout.flush()

if (len(sys.argv) > 1):
    text = sys.argv[1]
    freq_dist(text)

# url = 'http://www.gutenberg.org/files/8993/8993-h/8993-h.htm'
# request = requests.get(url)
# html = request.text
# soup = BeautifulSoup(html, "html5lib")
# tags = ['style', 'script', 'head', 'title', 'meta', '[document]', 'pre', 'table', 'a']
# for t in tags:
#     [s.extract() for s in soup(t)]
# text = soup.get_text()
# text = "I thought I saw a hippo in the sky. I'm sure I was wrong. The sun was shining too brightly for it to be true. I think the robots did it... In fact I am sure of it."
# freq_dist(text)