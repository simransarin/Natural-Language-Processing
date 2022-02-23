import glob
import os
import sys
import re
import json

def naive_bayes_learn(input_path, train_data):
    files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
    p_prob = {}
    prediction_count={'d_neg':0,'t_neg':0,'d_pos':0,'t_pos':0}
    
    read_input(files, train_data, prediction_count)
    count_literals(files, p_prob, prediction_count)
    cal_prob(train_data, p_prob)
        
def read_input(files, train_data, prediction_count):
    stopwords={"until", "am", "more", "most", "i", "we", "once", "their", "ourselves", "because", "yourselves", "ours", "our", "you", "with", "whom", "who", "he", "and", "him", "was", "his", "himself", "it", "as", "she", "she'd", "she'll", "she's", "her", "its", "I", "hers", "so", "against", "t", "than", "yourself", "too", "herself", "he'll", "he's", "itself", "you", "over", "further", "then", "between", "here", "there", "when", "under", "these", "what's", "when", "when's", "where", "where's","which", "while", "who's", "again", "your", "having", "do", "just", "does", "doing", "up", "down", "yours", "where", "my", "myself", "they", "where", "why", "how", "other", "or", "but", "of", "on", "off", "if", "are", "being", "while", "in", "out", "this", "me", "the", "into", "through", "at", "by", "for", "their", "during", "an", "have", "had", "has", "be", "been", "themselves", "them", "that", "before", "after", "above", "a", "theirs", "below", "to", "from", "up", "do", "does", "now"}
    for file in files:
        sfile=file.split('/')
        class2=sfile[-3]
        class1=sfile[-4]
        evaluate = open(file,'r').read()
        evaluate = re.sub(r'[^\w\s]', '', evaluate)
        evaluate = evaluate.split(' ')
        evaluate = [lexical_unit.lower() for lexical_unit in evaluate if lexical_unit not in stopwords]
        evaluate = [lexical_unit for lexical_unit in evaluate if lexical_unit.isalpha()]
        evaluateClass(class1, class2, evaluate, train_data, prediction_count)

def evaluateClass(class1, class2, evaluate, train_data, prediction_count):
    if class1 == 'positive_polarity':
        if class2 == 'deceptive_from_MTurk':
            train_data.append([evaluate,'d_pos'])
            prediction_count['d_pos']+=1
        else:
            train_data.append([evaluate,'t_pos'])
            prediction_count['t_pos']+=1
    else :
        if class2 == 'deceptive_from_MTurk':
            train_data.append([evaluate,'d_neg'])
            prediction_count['d_neg']+=1
        else:
            train_data.append([evaluate,'t_neg'])
            prediction_count['t_neg']+=1

def count_literals(files, p_prob, prediction_count):
    total_count = sum(prediction_count.values())
    for i in prediction_count:
        p_prob[i] = prediction_count[i]/total_count

def cal_prob(train_data, p_prob):
    word_count= {'d_neg':{},'t_neg':{},'d_pos':{},'t_pos':{}}
    word_set=set()
    for review,ans in train_data:
        for word in review:
            if word in word_count[ans]:
                word_count[ans][word]+=1
            else:
                word_count[ans][word]=1
    for j in ['d_neg','t_neg','d_pos','t_pos']:
        for i in list(word_count[j]):
            if word_count[j][i]<2:
                del word_count[j][i]
            else:
                word_set.add(i)
    alpha = 1.2

    l_prob= {'d_neg':{},'t_neg':{},'d_pos':{},'t_pos':{}}
    for word in word_set:
        for prob_ans in ['d_neg','t_neg','d_pos','t_pos']:
            if word in word_count[prob_ans]:
                l_prob[prob_ans][word] = (alpha+word_count[prob_ans][word])/(sum(word_count[prob_ans].values())+alpha*len(word_set))
            else:
                l_prob[prob_ans][word] = alpha/(sum(word_count[prob_ans].values())+alpha*len(word_set))
    model_file = open("nbmodel.txt","w")
    model_file.write(json.dumps(p_prob, indent=4))
    model_file.write(json.dumps(l_prob, indent=4))
    model_file.close()

        
train_data=[]
naive_bayes_learn(sys.argv[1], train_data)
