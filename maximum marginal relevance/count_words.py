import spacy
import os
import json
import string

PATH = '../samples/test/press_summary'
OUTFILE = '../samples/test_word_count_with_numbers.json'

nlp = spacy.load('en_core_web_md')

def count_word(text):
    doc = nlp(text)
    tokens = [t.text for t in doc]
    tokens = [t for t in tokens if len(t.translate(t.maketrans('', '', string.punctuation + string.whitespace))) > 0] # + string.digits
    #print(tokens)
    
    return len(tokens)
    

files = next(os.walk(PATH))[2]
d = {}
for fname in files:
    with open(os.path.join(PATH, fname)) as fp:
        cnt = count_word(fp.read())
        d[fname] = cnt

with open(OUTFILE, 'w') as fout:
    json.dump(d, fout)