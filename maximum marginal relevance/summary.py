import nltk
import json

class Summary:
    self.summary = []
    self.case = []
    # Load the tf-idfs created using tfidfs.py
    f = open("TF-IDFs.json", 'r')
    self.tfidfs = json.load(f)
    # The value of lambda
    self.l = 0.01

    def maximum_marginal_relevance(self, filename, sentence):
        """ Calculates the maximum marginal relavance for a sentence """
        # MMR(S i ) = λ sentence Sim(S i , Case) − (1 − λ) sentence Sim(S i , summary)
        return ((self.l * self.sim(filename, sentence, self.case) - ((1 - self.l) * self.sim(filename, sentence, self.summary))))

    def sim(self, filename, sentence, group):
        """ Calculates the similarity of a sentence with a group of sentences """
        total_count = len(group)
        total_sum = 0

        for compare_sentence in group:
            sentence_list = word_tokenize(sentence)
            compare_sentence_list = word_tokenize(compare_sentence)

            # sw contains the list of stopwords
            sw = stopwords.words('english')
            l1 = []
            l2 = []

            # Remove stop words from string
            sentence_set = {w for w in sentence_list if not w in sw}
            compare_sentence_set = {
                w for w in compare_sentence_list if not w in sw}

            # Form a set containing keys of both strings
            rvector = sentence_set.union(compare_sentence_set)

            # Create vectors to find cosine distance
            for w in rvector:
                if w in sentence_set:
                    l1.append(self.tfidfs[filename][sentence][w])
                else:
                    l1.append(0)
                if w in compare_sentence_set:
                    l2.append(self.tfidfs[filename][compare_sentence][w])
                else:
                    l2.append(0)
            c = 0

            # Cosine formula
            for i in range(len(rvector)):
                c += l1[i]*l2[i]
            cosine = c / float((sum(l1)*sum(l2))**0.5)
            total_sum += cosine

        # Return the average of similarity
        return total_sum/total_count
