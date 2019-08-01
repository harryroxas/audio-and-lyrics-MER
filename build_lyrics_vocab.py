import os
import sys
import sqlite3

from string import punctuation
from collections import Counter
from nltk.corpus import stopwords

def clean_lyric_tokens(tokens):
    #remove punctuation from each token
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    #remove tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    #filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    #filter out short tokens
    tokens = [word for word in tokens if len(word) > 2]

    return tokens

def add_lyrics_to_vocab(lyrics, vocab):
	# clean doc
	tokens = clean_lyric_tokens(lyrics)
	# update counts
	vocab.update(tokens)

all_tracks = []
all_labels = []
#Open track file and access track ids and their corresponding label
with open("track_tags2.txt") as f:
    for line in f:
        x = line.rstrip().split(None, 1)
        all_tracks.append(x[0])
        all_labels.append(eval(x[1])[0])

dblyrics = 'mxm_dataset.db' #DB for lyrics

if not os.path.isfile(dblyrics): #Check if DB exists
    print('ERROR: db file %s does not exist?' % dblyrics)

conn = sqlite3.connect(dblyrics) #Connect to DB

#GET THE LYRICS IN THE FORM OF Bag-of-words FOR EACH TRACk
lyrics = []
for tid in all_tracks:
    sql = "SELECT word, count FROM lyrics WHERE track_id='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchall()
    word = []
    for k in data:
        for count in range(k[1]):
            word.append(k[0])
    lyrics.append(word)

print(len(all_tracks), len(all_labels), len(lyrics))

#Create the Lyrics dataset
lyrics_data = {}
for k in range(len(all_tracks)):
    lyrics_data[all_tracks[k]] = [lyrics[k], all_labels[k]]

#Save the lyrics dataset to a file
with open("lyrics_dataset.txt", 'w') as f:
    for k in lyrics_data.keys():
        f.write("%s %s\n" % (k, lyrics_data[k]))

conn.close() #Close the DB connection