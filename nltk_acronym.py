# Author: Jack Keane
# Date: 3/25/20
# Description: Create acronym with given word using given data.

# Libraries
import pickle
from math import log10
from nltk import pos_tag
from nltk.corpus import cmudict, wordnet
from nltk.tokenize import word_tokenize

# Supplement data
prondict = cmudict.dict()
acronym_data = ["quotes", "shakespeare", "state_union", "inaugural", "bible", "all"]

# Constants
PENALTY = -10
SIM_LIMIT = .6
MAX_SEQUENCES = 250
START = "$"
END = "#"
NORMALIZE = "%"


# Code
def generate_acronym(word, data):
    """
    Creates acronym with given word and data.

    Parameters:
        word (str): Acronym will be created from this.
        data (str): String that will allow access to specific pickle file.

    Returns:
        list(str): List of top acronyms
    """

    pos_graph, word_graph, pos_word = load_data(data)

    first_scores = {}
    first_sequence = {}

    # For the first letter of acronym only.
    # Looks at every part of speech adjacent to start of sentence.
    for adj_pos in pos_graph[START].f1:
        if adj_pos != NORMALIZE:
            # Look at every word for part of speech.
            for w in pos_word[adj_pos]:
                # If match to acronym is found, determine if word is adjacent to start of sentence
                if w[0] == word[0] and w != word and (w in word_graph[START].f1 or rare_letter_check(w[0])):

                    # Calculate score.
                    pos_score = calculate(pos_graph[START].f1, adj_pos)
                    word_score = get_score(word_graph[START].f1, w)
                    try:
                        # Number of syllables according to prondict.
                        comp_score = len(max(prondict[w]))
                    except KeyError:
                        comp_score = 0
                    first_scores[(w, adj_pos)] = pos_score + word_score + comp_score

                    first_sequence[(w, adj_pos)] = [(START, START), (w, adj_pos)]

    # Limit sequences to top MAX_SEQUENCES
    current_scores, part_sequence = get_top_sequences(first_scores, first_sequence)

    # For rest of acronym.
    for i in range(1, len(word)):

        next_scores = {}
        next_part_sequence = {}

        for key in current_scores.keys():

            # Get previous two word/PoS pairs
            word_a = part_sequence[key][-2]
            word_b = part_sequence[key][-1]

            # Look at PoS adjacent to previous PoS
            for adj_pos in pos_graph[word_b[1]].f1:
                if adj_pos != NORMALIZE:
                    # Look at words for PoS
                    for w in pos_word[adj_pos]:
                        # If match to acronym is found, determine if word is adjacent to start of sentence
                        if w[0] == word[i] and (rare_letter_check(word[i-1:i+1]) or w in word_graph[word_b[0]].f1):

                            # If < 2 letters away from ending, consider adjacency to end of sentence
                            if i == len(word) - 2:
                                total_score = get_score(word_graph[w].f2, END) + \
                                              get_score(pos_graph[adj_pos].f2, END)
                            elif i == len(word) - 1:
                                total_score = get_score(word_graph[w].f1, END) + \
                                              get_score(pos_graph[adj_pos].f1, END)
                            else:
                                total_score = 0

                            # Calculate score
                            pos_score = calculate(pos_graph[word_b[1]].f1, adj_pos) + \
                                get_score(pos_graph[word_a[1]].f2, adj_pos)
                            word_score = get_score(word_graph[word_b[0]].f1, w) + \
                                get_score(word_graph[word_a[0]].f2, w)
                            try:
                                # Number of syllables according to prondict
                                comp_score = len(max(prondict[w]))
                            except KeyError:
                                comp_score = 0

                            total_score += current_scores[key] + pos_score + word_score + comp_score

                            # If word/PoS pair already exists, use pair with higher score
                            if not ((w, adj_pos) in next_scores and next_scores[(w, adj_pos)] > total_score):
                                next_scores[(w, adj_pos)] = total_score
                                next_part_sequence[(w, adj_pos)] = part_sequence[key].copy()
                                next_part_sequence[(w, adj_pos)].append((w, adj_pos))

        # Limit sequences to top MAX_SEQUENCES
        current_scores, part_sequence = get_top_sequences(next_scores, next_part_sequence)

    sen = ""
    acronyms = []

    # Create list of top acronyms
    sequences = sorted(current_scores, key=current_scores.get, reverse=True)
    while len(sequences) != 0 and len(acronyms) < 10:
        sentence = part_sequence[sequences.pop(0)][1:]
        for word in sentence:
            sen += word[0] + " "
        sen = sen.strip()
        if len(acronyms) == 0:
            acronyms.append(sen)
        else:
            res = True
            # Determine if acronym is unique to acronym list
            for a in acronyms:
                if sentence_similarity(a, sen) > SIM_LIMIT:
                    res = False
            if res:
                acronyms.append(sen)
        sen = ""

    return acronyms


def load_data(data):
    """
    Load data based on keyword.

    Parameters:
        data (str): Keyword

    Returns:
        pos_graph (dict): Dictionary of part of speech adjacency
        word_graph (dict): Dictionary of word adjacency
        pos_word (dict): Dictionary of words in each part of speech
    """

    pickle_in = open("acronym_data/" + data + "_data.pickle", "rb")
    ds = pickle.load(pickle_in)

    pos_graph = ds["pos_graph"]
    word_graph = ds["word_graph"]
    pos_word = ds["pos_word"]

    pickle_in.close()

    return pos_graph, word_graph, pos_word


def get_top_sequences(scores, sequences):
    """
    Gets top MAX_SEQUENCES of scores and sequences.

    Parameters:
        scores (dict): Dictionary of scores based on last word/PoS pair
        sequences (dict): Dictionary of sequences based on last word/PoS pair

    Returns:
        res_scores (dict): Dictionary of top MAX_SEQUENCES scores based on last word/PoS pair
        res_sequence (dict): Dictionary of top MAX_SEQUENCES sequences based on last word/PoS pair
    """

    top_scores = sorted(scores, key=scores.get, reverse=True)[:MAX_SEQUENCES]
    res_scores = {}
    res_sequence = {}

    for key in top_scores:
        res_scores[key] = scores[key]
        res_sequence[key] = sequences[key]

    return res_scores, res_sequence


def get_score(edge, node):
    """Get score based on adjacency. If there is no adjacency, place a penalty"""
    if node in edge:
        return calculate(edge, node)
    else:
        return PENALTY


def calculate(edge, node):
    """Calculate adjacency"""
    return log10(edge[node] / edge[NORMALIZE])


def rare_letter_check(substring):
    """Due to small amount of words starting with 'x' or 'z', make exception to open up possibilities."""
    return 1 in [c in substring for c in {"x", "z"}]


def penn_to_wn(tag):
    """
    Convert between a Penn Treebank tag to a simplified Wordnet tag.

    From https://nlpforhackers.io/wordnet-sentence-similarity/
    """

    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    """From https://nlpforhackers.io/wordnet-sentence-similarity/"""

    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wordnet.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """
    Compute the sentence similarity using Wordnet.

    From https://nlpforhackers.io/wordnet-sentence-similarity/
    """

    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = find_max([synset.path_similarity(ss) for ss in synsets2])

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # To account for case where similarity cannot be computed
    if count == 0:
        score = 1
        count = 1

    # Average the values
    score /= count
    return score


def find_max(a_list):
    """Find max float while accounting for NoneType values."""
    res = 0
    for a in a_list:
        if a is not None and a > res:
            res = a
    return res


"""Code to play with program"""
# test_word = "acronym"
# acronym_data = ["quotes", "shakespeare", "state_union", "inaugural", "bible", "all"]
# top_acro = generate_acronym(test_word, acronym_data[0])
# print(top_acro)
