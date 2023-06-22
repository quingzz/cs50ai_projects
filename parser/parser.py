import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S | VP P NP | NP VP NP | NP VP P NP 
NP -> N | Det NP | Adj N | Adj NP | NP Adv | NP P NP | NP N | 
VP -> V | VP Adv | Adv VP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # preprocess sentence
    sentence = sentence.lower()
    # tokenize sentence
    tokenized = nltk.word_tokenize(sentence)

    removed_words = set()
    for word in tokenized:
        # loop through each character and check if the word contains any alphabetical character
        if not any(char.isalpha() for char in word):
            # if not, remove word
            removed_words.add(word)

    tokenized = [w for w in tokenized if w not in removed_words]
    return tokenized


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    def dfs(tree: nltk.Tree, np_list: list):
        """Helper function to do 2 things:
        - reach lowest NP subtree of given tree and append it to np_list
        - check each subtree match condition of having no NP subtree & labeled as NP and add to np_list"""
        if len(tree.leaves()) == 1:
            # base case, when reach leaf, add it no np_list if label is NP
            # return True to top call to denote that NP node is available in this branch
            if tree.label() == "NP":
                if tree not in np_list:
                    np_list.append(tree)
                return True
            # return False otherwise
            return False

        # handle case when NP is not a leaf (tree that does not contain NP subtree)
        contains_NP = False
        for subtree in tree.subtrees():
            if subtree == tree:
                continue
            # use recursive call to check for NP subtree and add NP chunk
            if dfs(subtree, np_list) or subtree.label() == "NP":
                contains_NP = True

        # add tree to list if tree is NP and does not contains NP subtree
        if tree.label() == "NP" and not contains_NP:
            if tree not in np_list:
                np_list.append(tree)

        # return whether tree contains NP to top call
        return contains_NP

    result = list()
    dfs(tree, result)
    return result


if __name__ == "__main__":
    main()
