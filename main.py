from ForwardAlgorithm import calculateForwardAlgoLog, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgoLog
from Viterbi import hiddenStatePath, getLastState, calculateVeterbiEncodingLog
from helperFunctions import writeToFileWithBreaks, writeToFileWithBreaksStraight, stripAwayNewLines,writeToFileThreeCol, computePosteriorDecodingLog, calculatePosteriorMeanLog   

def mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, delim, initial):

    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)
    
    sequences = stripAwayNewLines(inputFile) #tuple pair of each sequence
    seqLength = len(sequences[0])   
    inputFile.close()
    print "Calculating Forward"
    forwardTableLog = calculateForwardAlgoLog(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )

    print "Calculatring Probability of Path"
    likelihood = likelihoodOfSequence(forwardTableLog)
    print "Calculating Backwards"
    backwardsTableLog = calculateBackwardsAlgoLog(transitionProbalities, emissionI, emissionD, sequences )
    print "Calculating Viterbi Encoding"
    veterbiEncodingLog = calculateVeterbiEncodingLog(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )
    veterbiStatesLog = hiddenStatePath(veterbiEncodingLog[1], seqLength, getLastState(veterbiEncodingLog[0],seqLength ))
     
    print "Calculating Most Probable States Posterior Encoding"
    posteriorTableAndRouteLog = computePosteriorDecodingLog(forwardTableLog, backwardsTableLog, seqLength, likelihood)# tuple pair. Has all post values and most probable
    posteriorStatesLog = posteriorTableAndRouteLog[1]
    posteriorMeanLog = calculatePosteriorMeanLog(posteriorTableAndRouteLog[0], seqLength, converstionTable)
    
    outputFile = open(delim +"/"+initial+"_veterbiEncoding_" + delim + ".txt", 'w')
    writeToFileWithBreaks(outputFile, veterbiStatesLog, converstionTable)
    print "Finished Writing Veterb Encoding for " + delim
    outputFile.close()
    
    outputFile2 = open(delim +"/"+initial+"_Posterior_"+ delim + ".txt", 'w')
    writeToFileWithBreaks(outputFile2, posteriorStatesLog, converstionTable)
    print "Finished Writing Posterior Encoding for " + delim
    outputFile2.close()
    
    outputFile3 = open(delim +"/"+initial+"_PosteriorMean_"+delim + ".txt", 'w')
    writeToFileWithBreaksStraight(outputFile3, posteriorMeanLog)
    print "Finished Writing Posterior Mean for " + delim
    outputFile3.close()
    
    outPutFile4 = open(delim +"/"+initial+"_ThreeCol_"+delim + ".txt", 'w')
    writeToFileThreeCol(outPutFile4, (veterbiStatesLog,posteriorStatesLog, posteriorMeanLog ), converstionTable)
    print "Finished Writing Three Columns for " + delim
    outPutFile4.close()
    
    outPutFile5 = open(delim +"/"+initial+"_likelihoods_"+delim + ".txt", 'w')
    outPutFile5.write(str(likelihood) + '\n')
    print "Finished Writing Log-likelihoods for " + delim
    outPutFile5.close()
    
    print "Done"
    
    
    