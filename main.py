from ForwardAlgorithm import calculateForwardAlgo, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgo
from Viterbi import calculateVeterbiEncoding,hiddenStatePath, getLastState
from helperFunctions import computePosteriorDecoding, writeToFileWithBreaks, calculatePosteriorMean, writeToFileWithBreaksStraight, stripAwayNewLines


def mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, delim):

    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)
    
    sequences = stripAwayNewLines(inputFile) 
    seqLength = len(sequences[0])   
    inputFile.close()
    print "Calculating Forward"
    forwardTable = calculateForwardAlgo(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    print "Calculatring Probability of Path"
    pathProbability = likelihoodOfSequence(forwardTable)
    print "Calculating Backwards"
    backwardsTable = calculateBackwardsAlgo(transitionProbalities, emissionI, emissionD, sequences )
    
    print "Calculating Viterbi Encoding"
    veterbiEncoding = calculateVeterbiEncoding(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    mostProbableStatesV = hiddenStatePath(veterbiEncoding[1], seqLength, getLastState(veterbiEncoding[0],seqLength ))
    print "Calculating Most Probable States Posterior Encoding"
    posteriorTableAndRoute = computePosteriorDecoding(forwardTable, backwardsTable, seqLength)
    
    posteriorMean = calculatePosteriorMean(posteriorTableAndRoute[0], seqLength, converstionTable)
    mostProbableStatesP = posteriorTableAndRoute[1]
    print "Done"
    
    
    outputFile = open("veterbiEncoding" + delim, 'w')
    writeToFileWithBreaks(outputFile, mostProbableStatesV, converstionTable)
    print "Finished Writing File"
    outputFile.close()
    
    
    
    outputFile2 = open("Posterior"+ delim, 'w')
    writeToFileWithBreaks(outputFile2, mostProbableStatesP, converstionTable)
    print "Finished Writing File 2"
    outputFile2.close()
    
    
    outputFile3 = open("PosteriorMean"+delim, 'w')
    writeToFileWithBreaksStraight(outputFile3, posteriorMean)
    print "Finished Writing File 3"
    outputFile3.close()
    
    
    
    
    
