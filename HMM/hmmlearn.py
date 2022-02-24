import json, sys
import math

class HMMLearn():
    def __init__(self, input_path):
        self.input_path = input_path
        self.processData(input_path)

    def processData(self, input_path):
        f = open(input_path, encoding = 'UTF-8')
        sentences = f.read()
        f.close()

        #dictionary of sentences -> lists of words
        sentenceList = sentences.splitlines()
        words = [sentence.split(" ") for sentence in sentenceList] 

        #Dictionary containing dictionary (tags: emmission prob) against tags
        transitionDict = {}
        transitionDict['_stag_'] = {}
        
        #Dictionary storing length of tags and tags
        tags = {}
        tags['_stag_'] = len(words)
        tags['_etag_'] = len(words)

        #Dictionary containing dictionary against words 
        emmissionDict = {}

        previous_tag = ''
        for sentence in words:
            previous_tag = '_stag_'
            for word in sentence:
                #list of the word and the tag
                wordTag = word.split("/")
                current_tag = wordTag[-1]#Get the tag here //change from -1 to 1
                if current_tag in tags:
                    tags[current_tag] += 1
                else:
                    tags[current_tag] = 1

                #emmission
                observation = word[:word.rfind("/")] #here the word will be saved 
                if observation in emmissionDict:
                    if current_tag in emmissionDict[observation]:#if the tag for a particular observation does'nt exist add word[:word.rfind("/")]] = 1;
                        emmissionDict[observation][current_tag] += 1
                    else:
                        emmissionDict[observation][current_tag] = 1
                else:
                    emmissionDict[observation] = dict()
                    emmissionDict[observation][current_tag] = 1   

                # transition tag
                if previous_tag in transitionDict:
                    if current_tag in transitionDict[previous_tag]:
                        transitionDict[previous_tag][current_tag] += 1
                    else:
                        transitionDict[previous_tag][current_tag] = 1                   
                else:
                    transitionDict[previous_tag] = dict()
                    transitionDict[previous_tag][current_tag] = 1
                previous_tag = current_tag

            if previous_tag in transitionDict:
                if '_etag_' in transitionDict[previous_tag]:
                    transitionDict[previous_tag]['_etag_'] += 1
                else:
                    transitionDict[previous_tag]['_etag_'] = 1                   
            else:
                transitionDict[previous_tag] = dict()
                transitionDict[previous_tag]['_etag_'] = 1

        smoothFact = 2#2
        leng =4*len(tags) -4#+ 2 #4*logtC+2
        
        for current_tag in tags:
            tags[current_tag] += leng
            if current_tag == '_etag_':
                continue
            for next_tag in tags:
                if next_tag == '_stag_':# newAddition
                    continue#newAddition
                if next_tag in transitionDict[current_tag]:
                    transitionDict[current_tag][next_tag] += smoothFact
                else:
                    transitionDict[current_tag][next_tag] = smoothFact
        self.calc_prob(tags, transitionDict, emmissionDict)

    def calc_prob(self, tags, transitionDict, emmissionDict):
        logFactor = 2*len(tags)
        for current_tag in transitionDict:
            for next_tag in transitionDict[current_tag]:
                transitionDict[current_tag][next_tag] = (math.log(transitionDict[current_tag][next_tag]) + logFactor) - math.log(tags[current_tag])

        for word in emmissionDict:
            for tag in emmissionDict[word]:
                emmissionDict[word][tag] = (math.log(emmissionDict[word][tag])+ logFactor) - math.log(tags[tag])

        self.model_write(tags, transitionDict, emmissionDict)

    def model_write(self, tags, transitionDict, emmissionDict):
        model_path = 'hmmmodel.txt'
        model_file = open(model_path, mode = 'w', encoding = 'UTF-8')
        model_file.write(json.dumps(tags))
        model_file.write("\n")
        model_file.write(json.dumps(emmissionDict))
        model_file.write("\n")
        model_file.write(json.dumps(transitionDict))
        model_file.close()

HMMLearn(sys.argv[1])