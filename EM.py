from helperFunctions import sameChars, normalizeCol

def highestColIndex(col):
    index = -1
    currentValue = -float('inf')
    for i in range(len(col)):
        if col[i] > currentValue:
            index = i
            currentValue = col[i]
    return index

def calculateBigADict(postTable):
    tableLength = len(postTable)
    results = {}
    laplaceOffset = 1
    
    for i in range(4):
        for j in range(4):
            results[(i,j)] = laplaceOffset
            
    for t in range(1, tableLength):
        currentIndexMax = highestColIndex(postTable[t])
        oldIndexMax = highestColIndex(postTable[t-1])
        tuplePair = (oldIndexMax, currentIndexMax)
        results[tuplePair] = results[tuplePair] + 1
        
    return results

def calculateETable(postTable, sequences):
    
    tableLength = len(postTable)
    laplaceOffset = 1
    results = [[0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset], 
               [0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset] ]
    for t in range(tableLength):
        currentIndexMax = highestColIndex(postTable[t])
        same = sameChars(sequences, t)
        iIndex = 0
        if same == False:
            iIndex = 1
        results[iIndex][currentIndexMax] = results[iIndex][currentIndexMax] + 1 
    return results

def calculatePosteriorExspected(postTable, sequences):
    startingIndex = highestColIndex(postTable[0])
    bigPi = [1,1,1,1]
    bigPi[startingIndex] =  bigPi[startingIndex] + 1
    bigADict = calculateBigADict(postTable)
    bigE = calculateETable(postTable, sequences)   # len = 2 len(len = 4
    return (bigPi, bigADict, bigE)


def sumTotalTransitions(tranDict, fromIndex):
    total = 0
    for i in range(4):
        if (fromIndex, i) in tranDict:
            total = total + tranDict[(fromIndex, i)]
    return total

def calculateLittleE(bigETable):
    emissionI = [0,0,0,0]
    emissionD = [0,0,0,0]
    
    for  i in range(4):
        totalEmissions = bigETable[0][i] + bigETable[1][i]
        if totalEmissions == 0:
            emissionI[i] = 0
            emissionD[i] = 0  
        else:
            emissionI[i] = float(bigETable[0][i]) / float(totalEmissions)    
            emissionD[i] = float(bigETable[1][i]) / float(totalEmissions)
    
    return (emissionI, emissionD)

def calculateNewInitialValues(bigValues):
    initialProbabilities = normalizeCol(bigValues[0])
    
    
    bigADict = bigValues[1]

    transitionProbalities = []
    for i in range(4):
        currentCol = []
        totalTransitionsAtI = sumTotalTransitions(bigADict, i)
        for j in range(4):
            if (i,j) in bigADict:
                currentCol.append(float(bigADict[(i,j)])/float(totalTransitionsAtI))
            else:
                currentCol.append(0.0)
        transitionProbalities.append(currentCol)
    
    
    emissionResults = calculateLittleE(bigValues[2])
    
    emissionI = emissionResults[0]
    emissionD = emissionResults[1]
    
    return (initialProbabilities, transitionProbalities, emissionI, emissionD)
    
    
    

