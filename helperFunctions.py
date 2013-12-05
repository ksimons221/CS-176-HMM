import math

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
    


def writeToFileThreeCol(aFile, indexes, encodingTable):
    for i in range(len(indexes[0])):
        tableIndexV = indexes[0][i]
        tableIndexP = indexes[1][i]
        meanP = indexes[2][i]
        strToWrite = str(encodingTable[tableIndexV]) + " " + str(encodingTable[tableIndexP]) + " " + str(meanP)
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
        toReturn = toReturn + (col[i] * convTable[i]) 
    return toReturn

def normalizeCol(singleCol):
    totalSum = 0
    for i in range(len(singleCol)):
        totalSum = totalSum + singleCol[i]
    if totalSum == 0:
        print singleCol
        exit(1)
    for i in range(len(singleCol)):
        singleCol[i] = float(singleCol[i]) / float(totalSum) 
    return singleCol

def logAdd( logX,  logY):
    if logY > logX:
        temp = logX
        logX = logY
        logY = temp
       
    if logX == -float("inf"):
        return logX;
    negDiff = logY - logX
    if negDiff < -20:
        return logX
    return logX + math.log(1.0 + math.exp(negDiff));

def sumAllLogProbailities(col):
    total1 = logAdd(col[0], col[1])
    total2 = logAdd(col[2], col[3])
    return logAdd(total1, total2)
        
def calculatePosteriorMean(postTable, seqLength, converstionTable):
    results = []
    for t in range(seqLength):
        currentCol = postTable[t]
        currentCol = normalizeCol(currentCol)
        averagePost = calcualteSinglePostMean(currentCol, converstionTable)
        results.append(averagePost)
    return results

def normalizeColLog(singleCol):
    maxInCol  = max(singleCol)
    for i in range(len(singleCol)):
        singleCol[i] = singleCol[i] - maxInCol 

    for i in range(len(singleCol)):
        singleCol[i] = math.exp(singleCol[i]) 

    totalSum = 0
    for i in range(len(singleCol)):
        totalSum = totalSum + singleCol[i]
        
    if totalSum == 0:
        print singleCol
        print "ERROR IN NORMALIZE COL LOG"
        exit(1)
    for i in range(len(singleCol)):
        singleCol[i] = singleCol[i] / totalSum 
    return singleCol

def calculatePosteriorMeanLog(postTable, seqLength, converstionTable):
    results = []


    for t in range(seqLength):
        currentCol = postTable[t]
        currentCol = normalizeColLog(currentCol)
        averagePost = calcualteSinglePostMean(currentCol, converstionTable)
        results.append(averagePost)
    return results

def computePosteriorDecoding(forwardTable, backwardTable, seqLength, likelihood):
    results = []
    mostProbableState = []
    for t in range(seqLength):
        currentValue = -1
        currentIndex = -1
        currentCol = []
        for i in range(4):
            value = (forwardTable[t][i] * backwardTable[t][i]) / likelihood
            if value > currentValue:
                currentValue = value
                currentIndex = i
            currentCol.append(value)
        results.append(currentCol)
        mostProbableState.append(currentIndex)
    return (results, mostProbableState)

def computePosteriorDecodingLog(forwardTable, backwardTable, seqLength, likelihood):
    results = []
    mostProbableState = []
    for t in range(seqLength):
        currentValue = -float("inf")
        currentIndex = -1
        currentCol = []
        for i in range(4):
            value = forwardTable[t][i] + backwardTable[t][i] - likelihood
            if value > currentValue:
                currentValue = value
                currentIndex = i
            currentCol.append(value)
        results.append(currentCol)
        mostProbableState.append(currentIndex)

    return (results, mostProbableState)
    