# Author: Jack Keane
# Date: 3/25/20
# Description: Convert inauguration speeches into csv

# Libraries
from nltk.corpus import inaugural
from nltk.tokenize import sent_tokenize
import string

# Code
speeches = inaugural.fileids()
f = open("../acronym_data/inaugural_data.csv", "w")

for s in speeches:
    speech = inaugural.raw(s)
    sentences = sent_tokenize(speech.lower().replace("â", ""))     # Remove symbol pair that appeared periodically
    for sen in sentences:
        f.write(sen.translate(str.maketrans('', '', string.punctuation)) + "\n")

f.close()
