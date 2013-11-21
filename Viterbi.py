from helperFunctions import generateEmissionValue

def calculateFirstProbabilies(initialProbabilities, emissionI, emissionD, sequences):
    firstCol = [0,0,0,0]

    for i in range(4):
        initialProb = initialProbabilities[i]
        emissionValue = generateEmissionValue(0, i, sequences, emissionI, emissionD)

        firstCol[i] = initialProb* emissionValue
    
    return firstCol


def calculateVeterbiEncoding(initialProbabilities, transitionProbalities, emissionI, emissionD, sequences ):
    
    results = [[0,0,0,0]]

    results[0] = calculateFirstProbabilies(initialProbabilities, emissionI, emissionD, sequences)
    endLength = len(sequences[0])
    backPointers = {}
    for t in range(1, endLength):
        currentCol = [0,0,0,0]
        for j in range(4):
            singleValue = 0
            emissionValue = generateEmissionValue(t, j, sequences, emissionI, emissionD)
            backIndex = 0
            for i in range(4):
                newValue = results[t-1][i]*transitionProbalities[i][j]
                if newValue > singleValue:
                    backIndex = i
                    singleValue = newValue
            backPointers[(t,j)] = backIndex
            currentCol[j] = singleValue * emissionValue
        results.append(currentCol)
            
    return (results, backPointers);


def getLastState(viterbiTable, seqeunceLength):
    lastIndex = seqeunceLength - 1
    maxValue = -1
    lastState = -1
    for i in range(4):
        value = viterbiTable[lastIndex][i]
        if value > maxValue:
            maxValue = value
            lastState = i
    return lastState

def hiddenStatePath(backPointers, seqeunceLength, lastState):
    results = [lastState]
    currentIndex = seqeunceLength-1
    currentState = lastState
    while currentIndex > 0:
        lastState = backPointers[(currentIndex,currentState)]
        results.insert(0, lastState)
        currentState = lastState
        currentIndex = currentIndex - 1
    return results
        