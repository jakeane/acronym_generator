# Author: Jack Keane
# Date: 3/25/20
# Description: Convert bible into csv

# Libraries
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
from string import digits, punctuation

# Code
bible = gutenberg.raw("bible-kjv.txt")
f = open("../acronym_data/bible_data.csv", "w")

b_no_digits = bible.translate(str.maketrans("", "", digits))
b_sentences = sent_tokenize(b_no_digits.replace(":", "").replace("\n", " "))
print(b_sentences[:10])
for sentence in b_sentences:
    f.write(sentence.translate(str.maketrans("", "", punctuation)).strip().lower() + "\n")
f.close()
