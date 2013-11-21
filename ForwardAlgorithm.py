from helperFunctions import generateEmissionValue

def likelihoodOfSequence(forwardTable):
    probabiltity = 0
    lastIndex = len(forwardTable) - 1
    for i in range(4):
        probability = probabiltity + forwardTable[lastIndex][i]
    return probability

def calculateFirstProbabilies(initialProbabilities, emissionI, emissionD, sequences):
    firstCol = [0,0,0,0]

    for i in range(4):
        initialProb = initialProbabilities[i]
        emissionValue = generateEmissionValue(0, i, sequences, emissionI, emissionD)

        firstCol[i] = initialProb* emissionValue
    
    return firstCol


def calculateForwardAlgo(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences ):
    
    results = [[0,0,0,0]]

    results[0] = calculateFirstProbabilies(initialProbabilities, emissionI, emissionD, sequences)
    endLength = len(sequences[0])
    for t in range(1, endLength):
        currentCol = [0,0,0,0]
        for j in range(4):
            singleValue = 0
            emissionValue = generateEmissionValue(t, j, sequences, emissionI, emissionD)
            for i in range(4):
                singleValue = singleValue + (results[t-1][i]*transitionProbalities[i][j])
            currentCol[j] = singleValue * emissionValue
        results.append(currentCol)
        
    #print results[4]
    
    return results;