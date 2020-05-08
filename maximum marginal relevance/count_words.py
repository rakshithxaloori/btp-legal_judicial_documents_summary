import spacy
import os
import json
import string

nlp = spacy.load('en_core_web_md')

def count_word(text):
    doc = nlp(text)
    tokens = [t.text for t in doc]
    tokens = [t for t in tokens if len(t.translate(t.maketrans('', '', string.punctuation + string.whitespace))) > 0] # + string.digits
    #print(tokens)
    
    return len(tokens)