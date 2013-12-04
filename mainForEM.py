from ForwardAlgorithm import calculateForwardAlgoLog, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgoLog
from EM import calculatePosteriorExspected, calculateNewInitialValues
from helperFunctions import  stripAwayNewLines, computePosteriorDecodingLog   

def mainRunnerEM(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, delim):
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

    likelihood = likelihoodOfSequence(forwardTableLog)

    print "Calculating Backwards"
    backwardsTableLog = calculateBackwardsAlgoLog(transitionProbalities, emissionI, emissionD, sequences )
     
    print "Calculating Most Probable States Posterior Encoding"
    posteriorTableAndRouteLog = computePosteriorDecodingLog(forwardTableLog, backwardsTableLog, seqLength)# tuple pair. Has all post values and most probable
    check = calculatePosteriorExspected(posteriorTableAndRouteLog[0], sequences)  #E
    temp = calculateNewInitialValues(check)  #M
    
    return (temp, likelihood) 