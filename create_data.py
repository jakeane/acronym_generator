# Author: Jack Keane
# Date: 3/25/20
# Description: Script that converts .csv data into adjacency data saved in .pickle

# Libraries
import nltk
from nltk.tokenize import word_tokenize
import pickle

# Own module
from data_scraping import qgn

# Constants
START = "$"
END = "#"

# Code
files = ["quotes", "shakespeare", "state_union", "inaugural", "bible", "all"]

for file in files:

    f = open("acronym_data/" + file + "_data.csv", "r")

    pos_graph = {}
    word_graph = {}
    pos_word = {}

    for line in f:

        tokens = word_tokenize(line)
        pos_tok = nltk.pos_tag(tokens)

        # Add sentence start/end signatures
        pos_tok.insert(0, (START, START))
        pos_tok.append((END, END))

        for i in range(len(pos_tok)):

            if pos_tok[i][0] not in word_graph:
                word_graph[pos_tok[i][0]] = qgn.QuoteGraphNode(pos_tok[i][0])
            word_graph[pos_tok[i][0]].add_word(pos_tok, i, 0)

            if pos_tok[i][1] not in pos_graph:
                pos_graph[pos_tok[i][1]] = qgn.QuoteGraphNode(pos_tok[i][1])
            pos_graph[pos_tok[i][1]].add_word(pos_tok, i, 1)

            if pos_tok[i][1] not in pos_word:
                pos_word[pos_tok[i][1]] = set()
            pos_word[pos_tok[i][1]].add(pos_tok[i][0])

    for node in pos_graph.values():
        node.normalize_by()
    for node in word_graph.values():
        node.normalize_by()

    ds = {"pos_graph": pos_graph, "word_graph": word_graph, "pos_word": pos_word}

    pickle_out = open("acronym_data/" + file + "_data.pickle", "wb")
    pickle.dump(ds, pickle_out)
    pickle_out.close()
    f.close()
