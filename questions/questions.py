import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_map = dict()

    for filename in os.listdir(directory):
        # get path to each file
        filedir = os.path.join(directory, filename)
        with open(filedir) as infile:
            content = infile.read()
            file_map[filename] = content

    return file_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # preprocess document
    document = document.lower()
    # tokenize
    tokenized = nltk.word_tokenize(document)

    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")

    # filter out punctuation and stopwords
    tokenized = [
        word for word in tokenized if word not in punctuation and word not in stopwords]

    return tokenized


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # dictionary storing word mapped to its idf value
    idf_map = dict()
    # get number of documents
    no_documents = len(documents)
    # dictionary storing word to list of documents containing it
    word_doc = dict()

    for document, words in documents.items():
        # loop through each word and save the list of documents containing it
        for word in words:
            if word not in word_doc:
                word_doc[word] = {document}

            word_doc[word].add(document)

    # compute idf for each word
    for word, docs in word_doc.items():
        idf_map[word] = math.log(no_documents / len(docs))

    return idf_map


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # dictionary storing filename mapped to corresponding sum of tf_idf values
    tf_idf = {document: 0 for document in files.keys()}

    for word in query:
        for filename, content in files.items():
            # skip if word in query not in content
            if word not in content:
                continue
            # add tf_idf for each word in query present in file to the sum for ranking
            # this works since query is a set and filename are keys -> no duplicate word, filename pair
            tf_idf[filename] += idfs[word]*content.count(word)

    # sort files based on their sum of tf-idf
    sorted_files = [k for k, v in sorted(
        tf_idf.items(), key=lambda item: item[1], reverse=True)]

    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_eval = dict()

    for sentence, tokens in sentences.items():
        matching_val = 0
        density_val = 0
        for word in query:
            # check if word is in the sentence
            if word in tokens:
                # compute matching values for each word
                # increase the matching counter
                matching_val += idfs[word]
                density_val += 1

        # compute final matching density
        density_val = density_val/len(tokens)
        sentence_eval[sentence] = (matching_val, density_val)

    sorted_sentence = [k for k, v in sorted(
        sentence_eval.items(), key=lambda item:item[1], reverse=True)]
    return sorted_sentence[:n]


if __name__ == "__main__":
    main()
