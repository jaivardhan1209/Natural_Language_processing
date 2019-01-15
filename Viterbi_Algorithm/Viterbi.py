# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:40:12 2018

@author: jvard
"""

## Viterbi Algorithm 
import sys

transProb = {'H-F':.3 , 'H-H':.7, 'F-H':.5, 'F-F':.5}
emissionProb = {'H-N':.1 , 'H-C':.4 , 'H-D':.5 , 'F-N':.6 , 'F-C':.3 , 'F-D':.1 }
startToHealthy = .6
startToFever = .4

#print(transProb)

print('--------------------------')

#print(emissionProb)

def FindMax(a,b):
    return a if a > b else b

def FindThePatternBasedOnObservation(obsPattern):
    patternLen = len(obsPattern)
    result = ''
    if patternLen <= 0:
        return result
    initialObservation = obsPattern[0]
    currentValueFromHealth = startToHealthy * emissionProb['H-' + initialObservation]
    currentValueFromFever = startToFever * emissionProb['F-' + initialObservation]
    state = 'H' if max(currentValueFromHealth, currentValueFromFever) == currentValueFromHealth else 'F'
    result = result + state
    
    #### do the same for all n-1 iteration over state using state as a sequence 
    for i in range(1 , patternLen):
        nextObservation = obsPattern[i]
        currentStateToHealthyForObs = transProb[state + '-' + 'H'] * emissionProb['H-' + nextObservation]
        currentStateToFeverForObs = transProb[state + '-' + 'F'] * emissionProb['F-'+ nextObservation]
        state = 'H' if max(currentStateToHealthyForObs, currentStateToFeverForObs) == currentStateToHealthyForObs else 'F'
        result = result + state       
    return result


if __name__ == "__main__":
    observationPattern = sys.argv[1]
    finalPrediction = FindThePatternBasedOnObservation(observationPattern)
    print(finalPrediction)



