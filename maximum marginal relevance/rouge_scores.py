import sys
import os
import json

from rouge import Rouge
from nltk.tokenize import sent_tokenize

rouge = Rouge()

if len(sys.argv) != 3:
    sys.exit(
        "Usage: python rouge_scores.py hypothesis_directory_path references_directory_path")

hyp_dir_path = sys.argv[1]
ref_dir_path = sys.argv[2]

# For each lambda, for each file
total_rouge_scores = list()

for eachLambda in os.listdir(hyp_dir_path):
    print("Calculating for lambda ", eachLambda[-3:], "...")
    # For each file in each lambda
    lambda_scores = dict()
    for hypFilename in os.listdir(hyp_dir_path + os.sep + eachLambda):
        print("     Calculating for file ",
              eachLambda, " ", hypFilename, "...")
        # Calculate the rouge scores
        # The name of the file is in the format --- <filename>.txt_summary
        # Delete the last 8 characters to get gold standard file
        refFilename = hypFilename[:-8]
        # Get the gold standard file from ref_dir_path
        with open(hyp_dir_path + os.sep + eachLambda + os.sep + hypFilename, 'r') as hyp_file, open(ref_dir_path + os.sep + refFilename, 'r') as ref_file:
            # Create a total sentence with hyp and ref and calculate the rouge scores
            hyp_sentence = ""
            ref_sentence = ""
            for sentence in sent_tokenize(hyp_file.read()):
                hyp_sentence += " " + sentence

            for sentence in sent_tokenize(ref_file.read()):
                ref_sentence += " " + sentence

            current_rouge_scores = rouge.get_scores(hyp_sentence, ref_sentence)
            lambda_scores[hypFilename] = current_rouge_scores

    total_rouge_scores.append({eachLambda: lambda_scores})

# Create a json file with these total rouge scores
json_file_path = os.path.join(os.getcwd(), "rouge_scores.json")
with open(json_file_path, 'w') as json_file:
    print("Dumping to json file...")
    json.dump({"rouge_scores": total_rouge_scores}, json_file)
