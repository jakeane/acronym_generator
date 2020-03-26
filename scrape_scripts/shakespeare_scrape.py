# Author: Jack Keane
# Date: 3/25/20
# Description: Convert Shakespeare plays into csv

# Libraries
from nltk.corpus import shakespeare
from nltk.tokenize import sent_tokenize
import string

# Code
play_list = shakespeare.fileids()
f = open("../acronym_data/shakespeare_data.csv", "w")

for p in play_list:
    play = shakespeare.xml(p)
    lines = play.findall("*/*/*/LINE")
    all_lines = ""
    for l in lines:
        all_lines += str(l.text).lower() + " "
    sentences = sent_tokenize(all_lines)
    for sen in sentences:
        f.write(sen.translate(str.maketrans('', '', string.punctuation)) + "\n")

f.close()
