import json, sys
import math

class HMMLearn():
    input_path = ""
    emmissionDict = {}
    transitionDict = {}
    tags = {}

    def __init__(self, input_path):
        self.input_path = input_path
        self.processData()
        self.emmissionDict = {}
        self.transitionDict = {}
        self.tags = {};

    def model_write(self):
        model_path = 'hmmmodel.txt'
        model_file = open(model_path, mode = 'w', encoding = 'UTF-8')
        model_file.write(json.dumps(self.tags))
        model_file.write("\n")
        model_file.write(json.dumps(self.emmissionDict))
        model_file.write("\n")
        model_file.write(json.dumps(self.transitionDict))
        model_file.close()

    def processData(self):
        f = open(self.input_path, encoding = 'UTF-8')
        sentences = f.read()
        f.close()

        #dictionary of sentences -> lists of words
        sentenceList = sentences.splitlines()
        words = [sentence.split(" ") for sentence in sentenceList] 

        #Dictionary containing dictionary (tags: emmission prob) against tags
        # transitionDict = {}
        self.transitionDict['_stag_'] = {}
        
        #Dictionary storing length of tags and tags
        # tags = {}
        self.tags['_stag_'] = len(words)
        self.tags['_etag_'] = len(words)

        #Dictionary containing dictionary against words 
        self.emmissionDict, previous_tag = {}, ''
        
        for sentence in words:
            previous_tag = '_stag_'
            for word in sentence:
                #list of the word and the tag
                wordTag = word.split("/")
                current_tag = wordTag[-1]
                if current_tag in self.tags:
                    self.tags[current_tag] += 1
                else:
                    self.tags[current_tag] = 1

                self.create_em_dict(word, current_tag)
                previous_tag = self.create_trx_dict(current_tag, previous_tag)

            if previous_tag in self.transitionDict:
                if '_etag_' in self.transitionDict[previous_tag]:
                    self.transitionDict[previous_tag]['_etag_'] += 1
                else:
                    self.transitionDict[previous_tag]['_etag_'] = 1                   
            else:
                self.transitionDict[previous_tag] = dict()
                self.transitionDict[previous_tag]['_etag_'] = 1

        smoothFact = 2
        leng =4*len(self.tags) -4
        
        for current_tag in self.tags:
            self.tags[current_tag] += leng
            if current_tag == '_etag_':
                continue
            for next_tag in self.tags:
                if next_tag == '_stag_':
                    continue
                if next_tag in self.transitionDict[current_tag]:
                    self.transitionDict[current_tag][next_tag] += smoothFact
                else:
                    self.transitionDict[current_tag][next_tag] = smoothFact
        self.calc_prob()

    def create_em_dict(self, word, current_tag):
        #emmission
        observation = word[:word.rfind("/")]
        if observation in self.emmissionDict:
            if current_tag in self.emmissionDict[observation]:
                self.emmissionDict[observation][current_tag] += 1
            else:
                self.emmissionDict[observation][current_tag] = 1
        else:
            self.emmissionDict[observation] = dict()
            self.emmissionDict[observation][current_tag] = 1  

    def create_trx_dict(self, current_tag, previous_tag):
         # transition tag
        if previous_tag in self.transitionDict:
            if current_tag in self.transitionDict[previous_tag]:
                self.transitionDict[previous_tag][current_tag] += 1
            else:
                self.transitionDict[previous_tag][current_tag] = 1                   
        else:
            self.transitionDict[previous_tag] = dict()
            self.transitionDict[previous_tag][current_tag] = 1
        return current_tag

    def calc_prob(self):
        logFactor = 2*len(self.tags)
        for word in self.emmissionDict:
            for tag in self.emmissionDict[word]:
                self.emmissionDict[word][tag] = (math.log(self.emmissionDict[word][tag])+ logFactor) - math.log(self.tags[tag])

        for current_tag in self.transitionDict:
            for next_tag in self.transitionDict[current_tag]:
                self.transitionDict[current_tag][next_tag] = (math.log(self.transitionDict[current_tag][next_tag]) + logFactor) - math.log(self.tags[current_tag])
        
        self.model_write()

    

HMMLearn(sys.argv[1])