import json, sys

class HMMDecode():
    input_path = ""
    emmissionDict = {}
    transitionDict = {}
    tags = {}

    def __init__(self, input_path, test_path):
        self.input_path = input_path
        self.test_path = test_path;
        self.tags, self.emmissionDict, self.transitionDict = self.processData(input_path)
        open_class_tags = self.createOpenClassTags()
        taggedSents = self.ViterbiAlgo(open_class_tags)
        self.output_write(taggedSents)

    def createOpenClassTags(self):
        open_class_tags = []
        tagof_unique_vocab = {}

        for tag in self.tags.keys():
            for word in self.emmissionDict.keys():
                if tag in self.emmissionDict[word].keys():
                    if tag in tagof_unique_vocab.keys():
                        tagof_unique_vocab[tag] += 1 
                    else: 
                        tagof_unique_vocab[tag] = 1

        for tag in tagof_unique_vocab.keys():
            if tagof_unique_vocab[tag]>0.1*len(self.emmissionDict.keys()):
                open_class_tags.append(tag)

        return open_class_tags

    def processData(self, input_path):
        dictionaries = [json.loads(x) for x in open(input_path, mode = 'r', encoding = 'UTF-8').read().split('\n')]
        tags = dictionaries[0]
        transitionDict = dictionaries[2]
        emmissionDict = dictionaries[1]
        return tags, emmissionDict, transitionDict

    def ViterbiFor0(self, wordList, Viterbi):
        firstWord = wordList[0]
        #Calculate Viterbi for first word
        Viterbi.append({})
        States ={}
        if firstWord in self.emmissionDict.keys():
            States = self.emmissionDict[firstWord]
        else:
            States = self.tags
        for tag in States.keys():
            if '_stag_' == tag:
                continue
            if firstWord in self.emmissionDict.keys():
                emissionProb = self.emmissionDict[firstWord][tag]
            else:
                emissionProb = 1
            Viterbi[0][tag]={}                                             
            Viterbi[0][tag]['desiredValue'] = '_stag_'
            Viterbi[0][tag]['probability'] = self.transitionDict['_stag_'][tag] * emissionProb  
        return Viterbi

    def ViterbiForLast(self, Viterbi, wordList):
        States = Viterbi[-1].keys()
        n = len(wordList)
        Viterbi.append({})
        maxProb ={'prob':0,'desiredValue':''}
        for tag in States:
            if '_etag_' == tag:
                continue
            tempProb = Viterbi[n-1][tag]['probability'] * self.transitionDict[tag]['_etag_'] 
            if(maxProb['prob']<tempProb):
                maxProb['prob'] = tempProb
                maxProb['desiredValue'] = tag
        Viterbi[-1]['_etag_']={}
        Viterbi[-1]['_etag_']['desiredValue'] = maxProb['desiredValue'] 
        Viterbi[-1]['_etag_']['probability'] = maxProb['prob']
        return Viterbi

    def ViterbiAlgo(self,open_class_tags):
        taggedSents = []
        f = open(self.test_path , encoding = 'UTF-8')
        allSentencesTest = f.read()
        sentencesListTest = allSentencesTest.splitlines()
        for sentence in sentencesListTest:
            Viterbi = []
            wordList = sentence.split()
            Viterbi = self.ViterbiFor0(wordList, Viterbi);
            
            #Start from word 1
            for i in range(1,len(wordList)):
                word = wordList[i]
                Viterbi.append({})
                if word in self.emmissionDict.keys():
                    States = self.emmissionDict[word]
                else:
                    States = self.tags
                for currTag in States.keys():
                    if currTag in [ '_etag_', '_stag_'] :
                        continue
                    if word in self.emmissionDict.keys():
                        emissionProb = self.emmissionDict[word][currTag]
                    else:
                        if currTag not in open_class_tags:
                            continue
                        emissionProb = 1
                    maxProb ={'prob':0,'desiredValue':''}

                    for prevTag in Viterbi[i-1].keys():
                        if prevTag in [ '_etag_', '_stag_']:
                            continue
                        tempProb = self.transitionDict[prevTag][currTag] * Viterbi[i-1][prevTag]['probability'] * emissionProb
                        if(tempProb>maxProb['prob']):
                            maxProb['desiredValue'] = prevTag
                            maxProb['prob'] = tempProb

                    Viterbi[i][currTag] = {}
                    Viterbi[i][currTag]['desiredValue'] = maxProb['desiredValue']
                    Viterbi[i][currTag]['probability'] = maxProb['prob']

            Viterbi = self.ViterbiForLast(Viterbi, wordList)
            taggedSents.append(self.tagSentence(Viterbi, wordList))
        return taggedSents

    def tagSentence(self, Viterbi, wordList):
        state = len(wordList)
        tag = '_etag_'
        iList = ""
        i = len(wordList)-1
        for i in range (len(wordList)-1, -1, -1):
            iList = wordList[i]+"/"+Viterbi[state][tag]['desiredValue']+" " + iList
            tag = Viterbi[state][tag]['desiredValue']
            state = state - 1
        return iList
    
    def output_write(self, taggedSents):
        output_path = 'hmmoutput.txt'
        output_file = open(output_path, mode = 'w', encoding = 'UTF-8')
        for sentence in taggedSents:
            output_file.write(sentence)
            output_file.write("\n")

HMMDecode("hmmmodel.txt", sys.argv[1])