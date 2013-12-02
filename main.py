from ForwardAlgorithm import calculateForwardAlgo, likelihoodOfSequence, calculateForwardAlgoLog
from BackwardsAlgorithm import calculateBackwardsAlgo, calculateBackwardsAlgoLog
from Viterbi import calculateVeterbiEncoding,hiddenStatePath, getLastState, calculateVeterbiEncodingLog
from helperFunctions import computePosteriorDecoding, writeToFileWithBreaks, calculatePosteriorMean, writeToFileWithBreaksStraight, stripAwayNewLines,writeToFileThreeCol, computePosteriorDecodingLog, calculatePosteriorMeanLog   
import math

def mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, delim):

    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)
    
    sequences = stripAwayNewLines(inputFile) #tuple pair of each sequence
    seqLength = len(sequences[0])   
    inputFile.close()
    print "Calculating Forward"
    #forwardTable = calculateForwardAlgo(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    forwardTableLog = calculateForwardAlgoLog(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )

    print "Calculatring Probability of Path"
    #likelihoods = likelihoodOfSequence(forwardTable)
    print "Calculating Backwards"
    #backwardsTable = calculateBackwardsAlgo(transitionProbalities, emissionI, emissionD, sequences )
    backwardsTableLog = calculateBackwardsAlgoLog(transitionProbalities, emissionI, emissionD, sequences )
    print "Calculating Viterbi Encoding"
    #veterbiEncoding = calculateVeterbiEncoding(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    print "Calculating Viterbi Encoding Log"

    veterbiEncodingLog = calculateVeterbiEncodingLog(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    
    
   # veterbiStates = hiddenStatePath(veterbiEncoding[1], seqLength, getLastState(veterbiEncoding[0],seqLength ))
    veterbiStatesLog = hiddenStatePath(veterbiEncodingLog[1], seqLength, getLastState(veterbiEncodingLog[0],seqLength ))

    

    print "Calculating Most Probable States Posterior Encoding"
    #posteriorTableAndRoute = computePosteriorDecoding(forwardTable, backwardsTable, seqLength)# tuple pair. Has all post values and most probable
    #posteriorStates = posteriorTableAndRoute[1]
    #posteriorMean = calculatePosteriorMean(posteriorTableAndRoute[0], seqLength, converstionTable)
     
    print "Calculating Most Probable States Posterior Encoding Log"
    posteriorTableAndRouteLog = computePosteriorDecodingLog(forwardTableLog, backwardsTableLog, seqLength)# tuple pair. Has all post values and most probable
    posteriorStatesLog = posteriorTableAndRouteLog[1]
    posteriorMeanLog = calculatePosteriorMeanLog(posteriorTableAndRouteLog[0], seqLength, converstionTable)
    
    outputFile = open("veterbiEncoding" + delim, 'w')
    writeToFileWithBreaks(outputFile, veterbiStatesLog, converstionTable)
    print "Finished Writing File"
    outputFile.close()
    
    outputFile2 = open("Posterior"+ delim, 'w')
    writeToFileWithBreaks(outputFile2, posteriorStatesLog, converstionTable)
    print "Finished Writing File 2"
    outputFile2.close()
    
    outputFile3 = open("PosteriorMean"+delim, 'w')
    writeToFileWithBreaksStraight(outputFile3, posteriorMeanLog)
    print "Finished Writing File 3"
    outputFile3.close()
    
    outPutFile4 = open("ThreeCol"+delim, 'w')
    writeToFileThreeCol(outPutFile4, (veterbiStatesLog,posteriorStatesLog, posteriorMeanLog ), converstionTable)
    print "Finished Writing File 4"
    outPutFile4.close()
    
    
