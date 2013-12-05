from ForwardAlgorithm import calculateForwardAlgoLog, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgoLog
from EM import calculateBigVars, calculateNewInitialValues
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

    forwardTable = calculateForwardAlgoLog(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences )

    likelihood = likelihoodOfSequence(forwardTable)

    backwardTable = calculateBackwardsAlgoLog(transitionProbalities, emissionI, emissionD, sequences )
     
    posteriorTableAndRouteLog = computePosteriorDecodingLog(forwardTable, backwardTable, seqLength, likelihood)# tuple pair. Has all post values and most probable
    check = calculateBigVars (posteriorTableAndRouteLog[0], sequences, forwardTable, backwardTable, transitionProbalities, emissionI, emissionD, likelihood) #E
    temp = calculateNewInitialValues(check)  #M    
    
    return (temp, likelihood) 