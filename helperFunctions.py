
def sameChars(sequences, index):
    char1 = sequences[0][index]
    char2 = sequences[1][index]
    if char1 == char2:
        return True
    else:
        return False
    
def writeToFileWithBreaksStraight(aFile, indexes):
    for i in range(len(indexes)):
        strToWrite = str(indexes[i])
        aFile.write(strToWrite + '\n')
    
def writeToFileWithBreaks(aFile, indexes, encodingTable):

    for i in range(len(indexes)):
        tableIndex = indexes[i]
        strToWrite = str(encodingTable[tableIndex])
        aFile.write(strToWrite + '\n')
    

def generateEmissionValue(indexInSequence, stateIndex, sequences, emissionI, emissionD):
   
    sameChar = sameChars(sequences, indexInSequence)
    emissionValue = 0
    if sameChar == True:
        emissionValue = emissionI[stateIndex]
    else:
        emissionValue = emissionD[stateIndex]
   
    return emissionValue;

def calcualteSinglePostMean(col, convTable):
    toReturn = 0
    for i in range(len(col)):
        toReturn = toReturn + (col[i] + convTable[i]) 
    return toReturn

def normalizeCol(singleCol):
    totalSum = 0
    for i in range(len(singleCol)):
        totalSum = totalSum + singleCol[i]
    for i in range(len(singleCol)):
        singleCol[i] = singleCol[i] / totalSum 
    return singleCol
        
def calculatePosteriorMean(postTable, seqLength, converstionTable):
    results = []
    for t in range(seqLength):
        currentCol = postTable[t]
        currentCol = normalizeCol(currentCol)
        averagePost = calcualteSinglePostMean(currentCol, converstionTable)
        results.append(averagePost)
    return results

def computePosteriorDecoding(forwardTable, backwardTable, seqLength):
    results = []
    
    mostProbableState = []
    
    for t in range(seqLength):
        currentValue = -1
        currentIndex = -1
        currentCol = []
        for i in range(4):
            value = forwardTable[t][i] * backwardTable[t][i]
            if value > currentValue:
                currentValue = value
                currentIndex = i
            currentCol.append(value)
        results.append(currentCol)
        mostProbableState.append(currentIndex)
    
    return (results, mostProbableState)

    