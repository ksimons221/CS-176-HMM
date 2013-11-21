from ForwardAlgorithm import calculateForwardAlgo, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgo
from Viterbi import calculateVeterbiEncoding,hiddenStatePath, getLastState
from helperFunctions import computePosteriorDecoding, writeToFileWithBreaks, calculatePosteriorMean, writeToFileWithBreaksStraight


def stripAwayNewLines(inputFile):
    seq1 = False
    sequence1 = ""
    sequence2 = ""
    for line in inputFile:
        line = line.rstrip('\n')
        dontAppend = False
        if line[0] == '>':
            dontAppend = True
            if seq1 == False:
                seq1 = True
            else:
                seq1 = False
        
        if dontAppend == False:
            if seq1:           
                sequence1 = sequence1 + line
            else:
                sequence2 = sequence2 + line 
            
    return (sequence1, sequence2)

initialProbabilities = [0.603154, 0.357419, 0.0388879, 0.000539295]

converstionTable = [0.3225476896193923, 1.7457611011583467, 4.5366202969211304, 9.40]


transitionProbalities = [
[0.999916, 0.0000760902, 8.27877e-6, 1.14809e-7],
[0.000128404, 0.999786, 0.0000848889,    1.17723e-6],
[0.000128404, 0.000780214, 0.999068, 0.0000235507],
[0.000128404, 0.000780214, 0.00169821, 0.997393]
]

emissionI =   [0.999608, 0.998334, 0.995844, 0.991548]
emissionD =  [0.000391695, 0.00166636, 0.00415567, 0.008452]
        
inputFileName = "sequences_mu.fasta"

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




outputFile = open("veterbiEncoding", 'w')
writeToFileWithBreaks(outputFile, mostProbableStatesV, converstionTable)
print "Finished Writing File"
outputFile.close()



outputFile2 = open("Posterior", 'w')
writeToFileWithBreaks(outputFile2, mostProbableStatesP, converstionTable)
print "Finished Writing File 2"
outputFile2.close()


outputFile3 = open("PosteriorMean", 'w')
writeToFileWithBreaksStraight(outputFile3, posteriorMean)
print "Finished Writing File 3"
outputFile3.close()





