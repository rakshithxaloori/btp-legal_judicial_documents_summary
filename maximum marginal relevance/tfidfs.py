import os
import sys
import nltk
import math
import json


def main():
    """ Calculate the TF-IDF for a corpus of documents."""

    if len(sys.argv) != 3:
        sys.exit(
            "Usage: python tfidfs.py summarization-corpus LIIOfIndia-corpus")
    print("Loading data...")
    print("Calculating term frequencies...")
    term_frequencies_corpus = _create_term_frequency_matrix(sys.argv[1])

    # Calculate IDFs
    print("Calculating inverse document frequencies...")
    idfs = _create_idf_matrix(sys.argv[2])

    # Save IDFs in a json file
    IDFS_JSON_FILE_PATH = os.path.join(os.getcwd(), "IDFs.json")
    with open(IDFS_JSON_FILE_PATH, 'w') as fout:
        # Sorting the data in descending order
        json.dump({k: v for k, v in sorted(idfs.items(),
                                           key=lambda item: item[1], reverse=True)}, fout)

    # Calculating TF-IFDs
    print("Calculating TF-IFDs...")
    tfidfs = dict()
    for filename in term_frequencies_corpus:
        tfidfs[filename] = dict()
        for sentence in term_frequencies_corpus[filename]:
            word_tf_idfs_matrix = dict()
            for word in term_frequencies_corpus[filename][sentence]:
                tf = term_frequencies_corpus[filename][sentence][word]
                if word not in idfs:
                    idfs[word] = 0
                word_tf_idfs_matrix[word] = tf*idfs[word]

            tfidfs[filename][sentence] = word_tf_idfs_matrix

    # Save TF-IDFs in a json file
    TF_IDFS_JSON_FILE_PATH = os.path.join(os.getcwd(), "TF-IDFs.json")
    with open(TF_IDFS_JSON_FILE_PATH, 'w') as fout:
        # Sorting the data in descending order
        json.dump(tfidfs, fout)


def _create_idf_matrix(directory):
    """ Calculate the idfs from available data """
    # Used on the extracted data, LIIOfIndia
    word_frequency_files = dict()
    total_documents = 0
    for year_folder in os.listdir(directory):
        # For each year
        for case_folder in os.listdir(os.path.join(directory, year_folder)):
            # For each case in the year
            case_folder_path = os.path.join(
                directory, (year_folder + os.sep + case_folder))
            for filename in os.listdir(case_folder_path):
                total_documents += 1
                # For each file in the case
                with open(os.path.join(case_folder_path, filename)) as f:

                    # Extract words
                    contents = {
                        word.lower() for word in nltk.word_tokenize(f.read()) if word.isalpha()
                    }

                    # Count frequencies
                    for word in contents:
                        if word not in word_frequency_files:
                            word_frequency_files[word] = 1
                        else:
                            word_frequency_files[word] += 1

    # Calculate the idf_matrix
    idf_matrix = dict()
    for word in word_frequency_files.keys():
        idf = math.log(total_documents / word_frequency_files[word])
        idf_matrix[word] = idf

    return idf_matrix


def _create_term_frequency_matrix(directory):
    """ Calculate the term matrix for each file """
    term_frequencies = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            term_frequencies[filename] = _create_tf_matrix(
                _create_frequency_matrix(nltk.sent_tokenize(f.read())))

    return term_frequencies


def _create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(nltk.corpus.stopwords.words("english"))

    for sent in sentences:
        freq_table = {}
        words = nltk.word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


if __name__ == "__main__":
    main()
