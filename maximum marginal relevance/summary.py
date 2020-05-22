import nltk
import json
import os
import math
import sys

from count_words import count_word


class Summary:
    def __init__(self):
        self.summary = list()
        self.case = list()

        # Count of the words
        print("Loading the counts...")
        self.count = dict()
        f = open("indian-summary-len-a1.txt", 'r')
        read_line = f.readline()
        while read_line != "":
            split_line = read_line.split(" ")
            self.count[split_line[0]] = int(split_line[1])
            read_line = f.readline()
        f.close()

        # Load the tf-idfs created using tfidfs.py
        print("Loading the tfidfs...")
        f = open("TF-IDFs.json", 'r')
        self.tfidfs = json.load(f)
        f.close()

        # The value of lambda
        self.l = 0.1

    def create_summary(self, directory):
        """ Takes a directory and creates the summaries of each file in the directory """
        # Create a directory with lambda as the name of the directory in the summaries
        print("Creating summaries")
        try:
            os.mkdir(os.path.join("summaries", ("summary - " + str(self.l))))
        except OSError as error:
            print(error)
        for filename in os.listdir(directory):
            print("Creating summary for ", filename)
            with open(os.path.join(directory, filename)) as f:
                self.case = nltk.sent_tokenize(f.read())
                count = 0
                while count < self.count[filename]:
                    maxValue = -math.inf
                    maxSentence = None
                    for sentence in self.case:
                        value = self._maximum_marginal_relevance(
                            filename, sentence)
                        if value > maxValue:
                            # Choose the maximum among them and add them to summary
                            maxValue = value
                            maxSentence = sentence

                    # Add this sentence to the summary
                    print("--------------------------------------")
                    print(maxSentence)
                    print(count_word(maxSentence))
                    count += count_word(maxSentence)
                    print(count)
                    print("--------------------------------------")
                    self.summary.append(maxSentence)
                    self.case.remove(maxSentence)

            # Re-order the sentences
            with open(os.path.join(directory, filename)) as f:
                total_doc = nltk.sent_tokenize(f.read())

            sentence_index = dict()
            # Store the indices in which the sentences appear
            for sentence in self.summary:
                sentence_index[sentence] = total_doc.index(sentence)

            # Order them according to the indices (values in the dict)
            ordered_sentences = {k: v for k, v in sorted(
                sentence_index.items(), key=lambda item: item[1])}

            with open(os.path.join(os.path.join("summaries", ("summary - " + str(self.l))), (filename + "_summary")), 'a') as fout:
                for sentence in ordered_sentences:
                    fout.write(sentence)
                    fout.write("\n")

            print("created summary for" + filename + "!")

            # Clear the summary, case
            self.summary.clear()
            self.case.clear()

    def _maximum_marginal_relevance(self, filename, sentence):
        """ Calculates the maximum marginal relavance for a sentence """
        # MMR(S i ) = λ sentence _Sim(S i , Case) − (1 − λ) sentence _Sim(S i , summary)
        return ((self.l * self._sim(filename, sentence, self.case) - ((1 - self.l) * self._sim(filename, sentence, self.summary))))

    def _sim(self, filename, sentence, group):
        """ Calculates the _similarity of a sentence with a group of sentences """
        if len(group) == 0:
            return 0

        total_count = len(group)
        total_sum = 0

        for compare_sentence in group:
            if sentence == compare_sentence:
                continue
            sentence_list = nltk.word_tokenize(sentence)
            compare_sentence_list = nltk.word_tokenize(compare_sentence)

            l1 = []
            l2 = []

            # Remove stop words from string
            sentence_set = {w for w in sentence_list}
            compare_sentence_set = {
                w for w in compare_sentence_list}

            # Form a set containing keys of both strings
            rvector = sentence_set.union(compare_sentence_set)

            # Create vectors to find cosine distance
            for w in rvector:
                if w in sentence_set:
                    try:
                        l1.append(self.tfidfs[filename][sentence][w.lower()])
                    except KeyError as error:
                        print(error)
                        print(filename, " --- ", sentence, " --- ", w.lower())
                        raise KeyError
                else:
                    l1.append(0)
                if w in compare_sentence_set:
                    try:
                        l2.append(self.tfidfs[filename]
                                  [compare_sentence][w.lower()])
                    except KeyError as error:
                        print(error)
                        print(filename, " --- ", compare_sentence,
                              " --- ", w.lower())
                        raise KeyError
                else:
                    l2.append(0)
            c = 0

            # Cosine formula
            for i in range(len(rvector)):
                c += l1[i]*l2[i]
            try:
                cosine = c / float((sum(l1)*sum(l2))**0.5)
            except ZeroDivisionError:
                continue
            total_sum += cosine

        # Return the average of _similarity
        return total_sum/total_count


def main():
    if len(sys.argv) != 2:
        sys.exit(
            "Usage: python summary.py summarization-corpus")
    summary = Summary()
    summarization_corpus = sys.argv[1]
    while summary.l <= 1.0:
        summary.create_summary(summarization_corpus)
        summary.l += 0.1


if __name__ == "__main__":
    main()
