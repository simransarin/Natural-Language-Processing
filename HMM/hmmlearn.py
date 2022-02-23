import time
start_time = time.time()
import json, sys
import math


def processData(input_path):
    sentences = open(input_path, encoding = 'UTF-8').read()

    #dictionary of sentences -> lists of words
    words = [sentence.split(" ") for sentence in sentences.splitlines()] 

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
            
        Smoothing(transitionDict, tags)
    
def Smoothing(transitionDict, emmissionDict, tags):
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
    calc_prob(tags, transitionDict, emmissionDict)

def calc_prob(tags, transitionDict, emmissionDict):
    logFactor = 2*len(tags)
    for current_tag in transitionDict:
        for next_tag in transitionDict[current_tag]:
            transitionDict[current_tag][next_tag] = (math.log(transitionDict[current_tag][next_tag]) + logFactor) - math.log(tags[current_tag])

    for word in emmissionDict:
        for tag in emmissionDict[word]:
            emmissionDict[word][tag] = (math.log(emmissionDict[word][tag])+ logFactor) - math.log(tags[tag])
    model_write(tags, transitionDict, emmissionDict)

def model_write(tags, transitionDict, emmissionDict):
    model_path = 'hmmmodel.txt'
    model_path = open(model_path, mode = 'w', encoding = 'UTF-8')
    model_path.write(json.dumps(tags) + "\n")
    model_path.write(json.dumps(emmissionDict) + "\n")
    model_path.write(json.dumps(transitionDict))

processData(sys.argv[1])