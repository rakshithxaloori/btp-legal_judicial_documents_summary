import os
import sys
import nltk
import math
import json

# For each year
    # For each case
        # For each file

def main():
    """ Calculate the TF-IDF for a corpus of documents."""

    if len(sys.argv) != 2:
        sys.etfidfsit("Usage: python etfidfstraction.py corpus")
    print("Loading data...")
    corpus = load_data(sys.argv[1])

    # Get all the words in corpus
    words = set()
    for filename in corpus:
        words.update(corpus[filename])

    # Calculate IDFs
    print("Calculating inverse document frequencies...")
    idfs = dict()
    for word in words:
        f = sum(word in corpus[filename] for filename in corpus)
        idf = math.log(len(corpus) / f)
        idfs[word] = idf

    # Calculating TF-IFDs
    print("Calculating TF-IFDs...")
    tfidfs = dict()
    for filename in corpus:
        tfidfs[filename] = []
        for word in corpus[filename]:
            tf = corpus[filename][word]
            tfidfs[filename].append((word, tf * idfs[word]))

    # Save TF-IDFS in a json file
    JSON_FILE_PATH = os.path.join(os.getcwd(), "TF-IDFs.json")
    with open(JSON_FILE_PATH, 'w') as fout:
        # Sorting the data in descending order
        json.dump({k: v for k, v in sorted(tfidfs.items(), key=lambda item: item[1], reverse=True)}, fout)


def load_data(directory):
    files = dict()
    for year_folder in os.listdir(directory):
        # For each year
        for case_folder in os.listdir(os.path.join(directory, year_folder)):
            # For each case in the year
            case_folder_path = os.path.join(directory, (year_folder + os.sep + case_folder))
            for filename in os.listdir(case_folder_path):
                # For each file in the case
                with open(os.path.join(case_folder_path, filename)) as f:

                    # Etfidfstract words
                    contents = [
                        word.lower() for word in nltk.word_tokenize(f.read()) if word.isalpha()
                    ]

                    # Count frequencies
                    frequencies = dict()
                    for word in contents:
                        if word not in frequencies:
                            frequencies[word] = 1
                        else:
                            frequencies[word] += 1
                    # Save the frequencies of each word of a file
                    files[filename] = frequencies

    return files

if __name__ == "__main__":
    main()