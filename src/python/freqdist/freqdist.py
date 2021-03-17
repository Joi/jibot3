import nltk
import requests
import hashlib
import sys
import matplotlib.pyplot as plt
import sqlite3
import os

stopwords = nltk.corpus.stopwords.words('english')
tokenizer = nltk.RegexpTokenizer(r"\w+")
conn = sqlite3.connect("/Users/margaretnottingham/Projects/jibot3/src/db/database.sqlite")

def plot(table, id, col):
    cur = conn.cursor()
    cur.execute(f"SELECT {col} FROM {table} WHERE id={id}")
    text = cur.fetchone()[0]
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
    if (len(sys.argv) == 5):
        command = sys.argv[1]
        table = sys.argv[2]
        id = sys.argv[3]
        col = sys.argv[4]
        eval(f"{command}('{table}', '{id}', '{col}')")
        # freq_dist(table, id, col)

if __name__ == '__main__':
    main()