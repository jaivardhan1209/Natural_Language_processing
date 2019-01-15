# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 19:11:40 2018

@author: jvard
"""

## parse the test file using nltk library and used to find the N-gram
from nltk import word_tokenize
from nltk.util import ngrams
import collections as coll
import pandas as pd
import sys

def getNgram(text, groupsize):
    token = word_tokenize(text)
    bigrams = ngrams(token,groupsize)
    return bigrams

def getBigramCountInCorpus(bigramCounter, corpus):
    ### loop through the biagram of sentence and find their occurance in complete corpus
    bigramCountDict = {}
    for key in bigramCounter:
        countPerBigram = corpus[key]
        #print(key)
        bigramCountDict[key] = countPerBigram
        
    return bigramCountDict

def findBigramProbability(bigramCounter, WordCountInCorpus):
    bigramProbabilityDict = {}
    for key in bigramCounter:
        countPerBigram = bigramCounter[key]
        totaloccurance = WordCountInCorpus[key[0]]
        bigramProbabilityDict[key] = countPerBigram / totaloccurance        
    return bigramProbabilityDict    

def findProbabilityofSentence(probabilityDictionary):
    prob = 1
    for key,value in probabilityDictionary.items():
        prob = prob * value
    return prob

def findBigramCountWithSmoothing(statementBigramCount, wordCountOfCorpus):
    ### loop through the biagram of sentence and find their occurance in complete corpus
    bigramCountDict = {}
    vocabcount = len(wordCountOfCorpus)
    for key in statementBigramCount:
        refinedCount = ((statementBigramCount[key] + 1) * wordCountOfCorpus[key[0]])/(wordCountOfCorpus[key[0]] + vocabcount)
        bigramCountDict[key] = refinedCount
    
    return bigramCountDict

def findBigramProbabilityWithSmoothing(bigramCounter, WordCountInCorpus):
    bigramProbabilityDict = {}
    vocabcount = len(WordCountInCorpus)
    for key in bigramCounter:
        countPerBigram = bigramCounter[key]
        totaloccurance = WordCountInCorpus[key[0]]
        bigramProbabilityDict[key] = (countPerBigram + 1 )/ (totaloccurance + vocabcount)        
    return bigramProbabilityDict        

def writeOutputInDataFrame(bigramDictionary):
    for key,value in bigramDictionary.items():
        print(key)
        df = pd.DataFrame.from_dict(value, orient='index').reset_index()
        columnName = 'probability' if 'Probability' in key else 'Count'
        df = df.rename(columns={'index':'Bigram', 0:columnName})
        print(df)
        
def writeProbabilityofSentence(probabilityDict):
    for key, value in probabilityDict.items():
        print(key)
        print(value)


def BiagramAlgorithm(corpus, statement1,statement2 ):
    #### Create the bigram from
    file = open("corpus.txt", "r",encoding="utf8")
    text = file.read()
    corpusBiagramlist = coll.Counter(getNgram(text,2))
    wordCountofCorpus = coll.Counter(text.split())

    # Bigram of statement defined
    statement1Bigram = coll.Counter(getNgram(statement1,2))
    statement2Bigram = coll.Counter(getNgram(statement2,2))

    resultSet = {}
    probabilityofStatementSet = {}
    ### Without add one smoothing ####
    statement1BigramCount = getBigramCountInCorpus(statement1Bigram,corpusBiagramlist)
    resultSet['Statement1 Bigram count without smoothing'] = statement1BigramCount
    statement2BigramCount = getBigramCountInCorpus(statement2Bigram,corpusBiagramlist)
    resultSet['Statement2 Bigram count without smoothing'] = statement2BigramCount
    probMatrixofstat1witoutsmooth = findBigramProbability(statement1BigramCount, wordCountofCorpus)
    resultSet['Probability metrix of statement1 without smoothing'] = probMatrixofstat1witoutsmooth
    probMatrixofstat2witoutsmooth = findBigramProbability(statement2BigramCount, wordCountofCorpus)
    resultSet['Probability metrix of statement2 without smoothing'] = probMatrixofstat2witoutsmooth
    probofStatement1 = findProbabilityofSentence(probMatrixofstat1witoutsmooth)
    probabilityofStatementSet['Probability of statement1 without smoothing'] = probofStatement1
    probofStatement2 = findProbabilityofSentence(probMatrixofstat2witoutsmooth)
    probabilityofStatementSet['Probability of statement2 without smoothing'] = probofStatement2

    #### with laplase smoothing or add one smoothing ########
    statement1BigramCountwithSmoothing = findBigramCountWithSmoothing(statement1BigramCount,wordCountofCorpus)
    resultSet['Statement1 Bigram count with smoothing'] = statement1BigramCountwithSmoothing
    statement2BigramCountwithSmoothing = findBigramCountWithSmoothing(statement2BigramCount,wordCountofCorpus)
    resultSet['Statement2 Bigram count with smoothing'] = statement2BigramCountwithSmoothing
    probMatrixofstat1withsmoothing = findBigramProbabilityWithSmoothing(statement1BigramCount, wordCountofCorpus)
    resultSet['Probability metrix of statement1 with smoothing'] = probMatrixofstat1withsmoothing
    probMatrixofstat2withsmoothing = findBigramProbabilityWithSmoothing(statement2BigramCount, wordCountofCorpus)
    resultSet['Probability metrix of statement2 with smoothing'] = probMatrixofstat2withsmoothing
    probofStatement1WithSmoothing = findProbabilityofSentence(probMatrixofstat1withsmoothing)
    probabilityofStatementSet['Probability of statement1 with smoothing'] = probofStatement1WithSmoothing
    probofStatement2WithSmoothing = findProbabilityofSentence(probMatrixofstat2withsmoothing)
    probabilityofStatementSet['Probability of statement2 with smoothing'] = probofStatement2WithSmoothing

    ##### write output on console in form of DataFrame ###################33
    writeOutputInDataFrame(resultSet)
    writeProbabilityofSentence(probabilityofStatementSet)


##### Main Method to call fileParser
if __name__ == "__main__":
    corpus = sys.argv[1]
    statement1 = sys.argv[2]
    statement2 = sys.argv[3]
    BiagramAlgorithm(corpus, statement1, statement2)