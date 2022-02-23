import glob
import string
import os
import sys
import re
import json


def naive_bayes_learn(input_path, train_data):
    files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
    prior_prob= {}
    prediction_count={'d_neg':0,'t_neg':0,'d_pos':0,'t_pos':0}
    
    read_input(files, prediction_count)
    count_literals(files, prior_prob, prediction_count)
    cal_prob(prior_prob)
        
def read_input(files, prediction_count):
        stopwords={"until", "am", "more", "most", "i", "we", "once", "their", "ourselves", "because", "yourselves", "ours", "our", "you", "with", "whom", "who", "he", "and", "him", "was", "his", "himself", "it", "as", "she", "she'd", "she'll", "she's", "her", "its", "I", "hers", "so", "against", "t", "than", "yourself", "too", "herself", "he'll", "he's", "itself", "you", "over", "further", "then", "between", "here", "there", "when", "under", "these", "what's", "when", "when's", "where", "where's","which", "while", "who's", "again", "your", "having", "do", "just", "does", "doing", "up", "down", "yours", "where", "my", "myself", "they", "where", "why", "how", "other", "or", "but", "of", "on", "off", "if", "are", "being", "while", "in", "out", "this", "me", "the", "into", "through", "at", "by", "for", "their", "during", "an", "have", "had", "has", "be", "been", "themselves", "them", "that", "before", "after", "above", "a", "theirs", "below", "to", "from", "up", "do", "does", "now"}
        for file in files:
            val=file.split('/')
            value_Class2=val[-3]
            value_Class1=val[-4]
            review = open(file,'r').read()
            review = re.sub(r'[^\w\s]', '', review).split(' ')
            review = [word.lower() for word in review if word not in stopwords]
            review = [word for word in review if word.isalpha()]
            print(review)
            if value_Class1 == 'positive_polarity':
                if value_Class2 == 'deceptive_from_MTurk':
                    self.train_data.append([review,'pos_dec'])
                    self.prediction_count['pos_dec']+=1
                else:
                    self.train_data.append([review,'pos_tru'])
                    self.prediction_count['pos_tru']+=1
            else :
                if value_Class2 == 'deceptive_from_MTurk':
                    self.train_data.append([review,'neg_dec'])
                    self.prediction_count['neg_dec']+=1
                else:
                    self.train_data.append([review,'neg_tru'])
                    self.prediction_count['neg_tru']+=1

            

    def count_literals(files, prior_prob, prediction_count):
        total_count = 0
        total_count = sum(self.prediction_count.values())
        for i in self.prediction_count:
            self.prior_prob[i] = self.prediction_count[i]/self.total_count
        #print(self.prior_prob) 

    def cal_prob(prior_prob):
        word_count= {'d_neg':{},'t_neg':{},'d_pos':{},'t_pos':{}}
        l_prob= {'d_neg':{},'t_neg':{},'d_pos':{},'t_pos':{}}
        word_set=set()
        for review,ans in self.train_data:
            for word in review:
                if word in self.word_count[ans]:
                    self.word_count[ans][word]+=1
                else:
                    self.word_count[ans][word]=1
        print(self.word_count)
        
        for j in ['neg_dec','neg_tru','pos_dec','pos_tru']:
            for i in list(self.word_count[j]):
                if self.word_count[j][i]<2:
                    del self.word_count[j][i]
                else:
                    self.word_set.add(i)
        alpha = 1.2
        for review_word in self.word_set:
            for prob_ans in ['neg_dec','neg_tru','pos_dec','pos_tru']:
                if review_word in self.word_count[prob_ans]:
                    self.l_prob[prob_ans][review_word] = (alpha+self.word_count[prob_ans][review_word])/(sum(self.word_count[prob_ans].values())+alpha*len(self.word_set))
                else:
                    self.l_prob[prob_ans][review_word] = alpha/(sum(self.word_count[prob_ans].values())+alpha*len(self.word_set))
        #print(self.l_prob)
        f = open("nbmodel.txt","w")
        f.write(json.dumps(self.prior_prob, indent=4))
        f.write(json.dumps(self.l_prob, indent=4))
        f.close()

        
train_data=[]
naive_bayes_learn(sys.argv[1], train_data)
