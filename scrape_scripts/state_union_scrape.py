# Author: Jack Keane
# Date: 3/25/20
# Description: Convert state of the union speeches into csv

# Libraries
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
import string

# Code
speeches = state_union.fileids()
f = open("../acronym_data/state_union_data.csv", "w")

for s in speeches:
    speech = state_union.raw(s)
    sentences = sent_tokenize(speech.lower().replace("\n", " "))
    for sen in sentences:
        f.write(sen.translate(str.maketrans('', '', string.punctuation)) + "\n")

f.close()
