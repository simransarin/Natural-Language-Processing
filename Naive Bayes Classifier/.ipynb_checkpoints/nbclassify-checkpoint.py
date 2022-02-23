import json
import sys
import re
import os
import math
import string
import glob

from string import digits


def initialise_env(input_path):
    files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
    return files


def read_input(files, test_data):
    stopwords = {"until", "am", "more", "most", "i", "we", "once", "their", "ourselves", "because", "yourselves", "ours", "our", "you", "with", "whom", "who", "he", "and", "him", "was", "his", "himself", "it", "as", "she", "she'd", "she'll", "she's", "her", "its", "I", "hers", "so", "against", "t", "than", "yourself", "too", "herself", "he'll", "he's", "itself", "you", "over", "further", "then", "between", "here", "there", "when", "under", "these", "what's", "when", "when's", "where", "where's",
                 "which", "while", "who's", "again", "your", "having", "do", "just", "does", "doing", "up", "down", "yours", "where", "my", "myself", "they", "where", "why", "how", "other", "or", "but", "of", "on", "off", "if", "are", "being", "while", "in", "out", "this", "me", "the", "into", "through", "at", "by", "for", "their", "during", "an", "have", "had", "has", "be", "been", "themselves", "them", "that", "before", "after", "above", "a", "theirs", "below", "to", "from", "up", "do", "does", "now"}
    for file in files:
        evaluate = open(file, 'r').read()
        evaluate = re.sub(r'[^\w\s]', '', evaluate).split(' ')
        evaluate = evaluate.lower()
        evaluate = evaluate.split()
        evaluate = [
            lexical_unit for lexical_unit in evaluate if lexical_unit not in stopwords]
        evaluate = [
            lexical_unit for lexical_unit in evaluate if lexical_unit.isalpha()]
        test_data.append([evaluate, file])
    naiveBayesClassify(test_data)


def naiveBayesClassify(test_data):
    predictions = ['d_neg', 't_pos', 'd_pos', 't_neg']
    with open('nbmodel.txt', 'r') as input_file:
        text = input_file.read().replace('}{', '},{')
        json_text = json.loads(f'[{text}]')
        p_prob = json_text[0]
        l_prob = json_text[1]
    output_file = open('nboutput.txt', 'w')
    for i in range(len(test_data)):
        pred_value = {}
        for probs in predictions:
            predict = 0
            for lexical_unit in test_data[i][0]:
                if lexical_unit in l_prob[probs]:
                    value = (l_prob[probs][lexical_unit])
                    predict += math.log(value)
            predict += math.log(p_prob[probs])
            pred_value[probs] = predict
        predict = max(pred_value, key=pred_value.get)
        if predict == 'd_neg':
            output_file.write("deceptive negative "+test_data[i][1])
            output_file.write("\n")
        elif predict == 't_pos':
            output_file.write("truthful positive "+test_data[i][1])
            output_file.write("\n")
        elif predict == 'd_pos':
            output_file.write("deceptive positive "+test_data[i][1])
            output_file.write("\n")
        elif predict == 't_neg':
            output_file.write("truthful negative "+test_data[i][1])
            output_file.write("\n")

    output_file.close()


test_data = []
read_input(initialise_env(sys.argv[1]), test_data)
