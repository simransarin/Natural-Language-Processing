import json, sys

class HMMDecode():
    def __init__(self, input_path, test_path):
        self.input_path = input_path
        self.test_path = test_path;
        tags, emmissionDict, transitionDict, open_class_tags = self.processData(input_path)
        taggedSents = self.ViterbiAlgo(tags,emmissionDict,transitionDict, open_class_tags, test_path)
        self.output_write(taggedSents)

    def processData(self, input_path):
        dictionaries = [json.loads(x) for x in open(input_path, mode = 'r', encoding = 'UTF-8').read().split('\n')]
        tags = dictionaries[0]
        emmissionDict = dictionaries[1]
        transitionDict = dictionaries[2]


        open_class_tags = []
        tagof_unique_vocab = {}

        for tag in tags.keys():
            for word in emmissionDict.keys():
                if tag in emmissionDict[word].keys():
                    if tag in tagof_unique_vocab.keys():
                        tagof_unique_vocab[tag] += 1 
                    else: 
                        tagof_unique_vocab[tag] = 1

        for tag in tagof_unique_vocab.keys():
            if tagof_unique_vocab[tag]>0.0350*len(emmissionDict.keys()):
                open_class_tags.append(tag)

        return tags, emmissionDict, transitionDict, open_class_tags

    def ViterbiAlgo(self, tags, emmissionDict, transitionDict, open_class_tags, test_path):
        f = open(test_path , encoding = 'UTF-8')
        allSentencesTest = f.read()
        sentencesListTest = allSentencesTest.splitlines()
        taggedSents = []
        for sentence in sentencesListTest:
            wordList = sentence.split()
            firstWord = wordList[0]
            Viterbi = []#Viterbi is a 3D  Dictionary containing word as the state, all tags for each state
            
            #Calculate Viterbi for first word
            Viterbi.append({})
            States ={}
            if firstWord in emmissionDict.keys():
                States = emmissionDict[firstWord] #dictionary
            else:
                States = tags
            for tag in States.keys():
                if tag == '_stag_':
                    continue
                if firstWord in emmissionDict.keys():
                    emissionProb = emmissionDict[firstWord][tag]
                else:
                    emissionProb = 1
                Viterbi[0][tag]={}
                Viterbi[0][tag]['probability'] = transitionDict['_stag_'][tag] * emissionProb                                               
                Viterbi[0][tag]['backpointer'] = '_stag_'
            
            print(open_class_tags)
            #Start from word 1
            for i in range(1,len(wordList)):
                word = wordList[i]
                Viterbi.append({})
                if word in emmissionDict.keys():
                    States = emmissionDict[word]
                else:
                    States = tags
                for currTag in States.keys():
                    if currTag == '_stag_' or currTag == '_etag_':
                        continue
                    if word in emmissionDict.keys():
                        emissionProb = emmissionDict[word][currTag]
                    else:
                        if currTag not in open_class_tags:
                            continue
                        emissionProb = 1
                    maxProb ={'prob':0,'backpointer':''}

                    for prevTag in Viterbi[i-1].keys():
                        if prevTag == '_stag_' or prevTag == '_etag_':
                            continue
                        tempProb = Viterbi[i-1][prevTag]['probability'] * \
                                    transitionDict[prevTag][currTag] * \
                                    emissionProb
                        if(tempProb>maxProb['prob']):
                            maxProb['prob'] = tempProb
                            maxProb['backpointer'] = prevTag

                    Viterbi[i][currTag] = {}
                    Viterbi[i][currTag]['probability'] = maxProb['prob']
                    Viterbi[i][currTag]['backpointer'] = maxProb['backpointer']

            #Do for End
            States = Viterbi[-1].keys()
            n = len(wordList)
            Viterbi.append({})
            maxProb ={'prob':0,'backpointer':''}
            for tag in States:
                if tag == '_etag_':
                    continue
                tempProb = Viterbi[n-1][tag]['probability'] * \
                                    transitionDict[tag]['_etag_'] 
                if(tempProb>maxProb['prob']):
                    maxProb['prob'] = tempProb
                    maxProb['backpointer'] = tag
            Viterbi[-1]['_etag_']={}
            Viterbi[-1]['_etag_']['probability'] = maxProb['prob']
            Viterbi[-1]['_etag_']['backpointer'] = maxProb['backpointer'] 
            taggedSents.append(self.tagSentence(Viterbi, wordList))
        return taggedSents

    def tagSentence(self, Viterbi, wordList):
        state = len(wordList)
        tag = '_etag_'
        iList = ""
        i = len(wordList)-1
        while i >= 0:
            iList = wordList[i]+"/"+Viterbi[state][tag]['backpointer']+" " + iList
            tag = Viterbi[state][tag]['backpointer']
            state -= 1
            i-=1
        return iList
    
    def output_write(self, taggedSents):
        output_path = 'hmmoutput.txt'
        output_file = open(output_path, mode = 'w', encoding = 'UTF-8')
        for sentence in taggedSents:
            output_file.write(sentence)
            output_file.write("\n")

HMMDecode("hmmmodel.txt", sys.argv[1])