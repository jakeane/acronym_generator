# Author: Jack Keane
# Date: 3/25/20
# Description: Trigram adjacency graph node


class QuoteGraphNode:
    """
    Trigram adjacency graph node.

    Attributes:
        name (str): Name of node
        f1 (dict): Keys are the names of nodes that immediately follow current node. Values are frequencies.
        f2 (dict): Same as above, but for nodes that are two edges away.
        NORMALIZE (str): Symbol that denotes the sum of frequencies in each f1 and f2.
    """

    def __init__(self, name):
        self.name = name
        self.f1 = {}
        self.f2 = {}
        self.NORMALIZE = "%"

    def add_word(self, sentence_list, index, g_type):
        """
        Add adjacent values to node.

        Parameters:
            sentence_list (list(str)): Tokenized sentence
            index (int): Index of node in sentence
            g_type (int): Distinguish between word and part of speech
        """

        if index <= len(sentence_list) - 2:                         # Check if index + 1 can be accessed
            if sentence_list[index + 1][g_type] in self.f1:         # Check if adjacent value already exists
                self.f1[sentence_list[index + 1][g_type]] += 1
            else:
                self.f1[sentence_list[index + 1][g_type]] = 1

        if index <= len(sentence_list) - 3:                         # Check if index + 2 can be accessed
            if sentence_list[index + 2][g_type] in self.f2:         # Check if adjacent value already exists
                self.f2[sentence_list[index + 2][g_type]] += 1
            else:
                self.f2[sentence_list[index + 2][g_type]] = 1

    def normalize_by(self):
        """Calculate sum of frequencies for each adjacency, then add to respective dictionary"""
        num = 0
        for freq in self.f1.values():
            num += freq
        self.f1[self.NORMALIZE] = num

        num = 0
        for freq in self.f2.values():
            num += freq
        self.f2[self.NORMALIZE] = num

    def __str__(self):
        return "Name: " + self.name + " F1: " + str(self.f1) + " F2: " + str(self.f2)
