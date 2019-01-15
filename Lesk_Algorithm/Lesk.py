# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:05:29 2018

@author: jvard
"""

from nltk.corpus import wordnet as wn
import nltk
import sys

## we need to consider only Noun, Verb, adverb and adjective
def Simplified_Lesk(word, sentence):
    max_overlap = 0
    synsets = wn.synsets(word)
    wordsence = synsets[0]
    synset_Gloss_Example = []
    print('----------------')
    print('Possible Synset: Overlapping Word')
    print('----------------')
    for synset in synsets:
        synset_Gloss_Example.clear()
        synset_Gloss_Example.append(FilterWordsToCaptureOnlyReleventPos(synset.definition()))
        for example in synset.examples():
              synset_Gloss_Example.append(FilterWordsToCaptureOnlyReleventPos(example)) 
        overlap = findOverlapWithSentence(synset_Gloss_Example, FilterWordsToCaptureOnlyReleventPos(sentence))
        print(synset , ':', overlap)
        if len(overlap) > max_overlap:
            max_overlap = len(overlap)
            wordsence = synset
    
    return wordsence

### only use noun, verb, adverb, adj to predict the sense
def FilterWordsToCaptureOnlyReleventPos(sentence):
    releventWord = []
    text = nltk.word_tokenize(sentence)
    text = nltk.pos_tag(text)
    releventTagList = ['NN', 'NNP', 'NNS', 'NNPS', 'VB', 'VBD', 'VBG','VBN','VBP','VPZ','JJ','JJR','JJS', 'RB','RBR','RBS']
    for pair in text:
        if pair[1] in releventTagList:
            releventWord.append(pair[0])
    return releventWord
    
    
    
def findOverlapWithSentence(synset_gloss_example, sentence):
    overlap = []
    for word in sentence:
        for item in synset_gloss_example:
            for corpousWord in item:
                if corpousWord.lower() == word.lower():
                    overlap.append(corpousWord)
    return set(overlap)


if __name__ == "__main__":
    word = sys.argv[1]
    sentence = sys.argv[2]
    maximumsense = Simplified_Lesk(word, sentence)
    print("-------------------")
    print('Final chosen sense:')
    print("-------------------")
    print(maximumsense, ':' , maximumsense.definition())
    
    
