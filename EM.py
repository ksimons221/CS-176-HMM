from helperFunctions import sameChars, normalizeCol, logAdd, generateEmissionValue, normalizeColLog
import math

def highestColIndex(col):
    index = -1
    currentValue = -float('inf')
    for i in range(len(col)):
        if col[i] > currentValue:
            index = i
            currentValue = col[i]
    return index

def calculateBigADict(postTable, laplaceOffset,sequences, forwardTable, backwardTable, transitionTable, emissionI, emissionD, likelihood):
    tableLength = len(postTable)
    results = {}
    
    for i in range(4):
        for j in range(4):
            results[(i,j)] = laplaceOffset
            
    for t in range(0, tableLength-1):
        for i in range(4):
            for j in range(4):
                eValue = generateEmissionValue(t, j, sequences, emissionI, emissionD)
                numerator = forwardTable[t][i]
                numerator = numerator + math.log(transitionTable[i][j]) 
                numerator = numerator + math.log(eValue) 
                numerator = numerator + backwardTable[t+1][j]
                denominator = likelihood
                total = numerator  -  denominator
                prob = math.exp(total)
                if prob == 0:
                    print "error in big A dict"
                    exit(1)
                results[(i,j)] = results[(i,j)] +  prob
        
    return results

def calculateETable(postTable, sequences, laplaceOffset):
    tableLength = len(postTable)
    results = [[0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset], 
               [0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset,0 +laplaceOffset] ]
    for t in range(tableLength):
        col = postTable[t]
        same = sameChars(sequences, t)
        iIndex = 0
        if same == False:
            iIndex = 1
        for i in range(4):
            if results[iIndex][i] == 0:
                results[iIndex][i] = col[i]
            else:
                results[iIndex][i] = logAdd(results[iIndex][i], col[i])
    for i in range(4):
        row = [results[0][i], results[1][i]]
        rowNormal = normalizeColLog(row)
        results[0][i] = rowNormal[0]
        results[1][i] = rowNormal[1]
    return results

def calculateBigPi(postTable, bigPi):
    col = normalizeColLog(postTable[0])
    for i in range(4):
        bigPi[i] = bigPi[i] + col[i]
    return bigPi

def calculateBigVars(postTable, sequences, forwardTable, backwardTable, transitionTable, emissionI, emissionD, likelihood):
    laplaceOffset = 0
    bigPi = [laplaceOffset,laplaceOffset,laplaceOffset,laplaceOffset]
    bigPi = calculateBigPi(postTable, bigPi)

    bigADict = calculateBigADict(postTable, laplaceOffset,sequences, forwardTable, backwardTable, transitionTable, emissionI, emissionD, likelihood)
    bigE = calculateETable(postTable, sequences, laplaceOffset)   # len = 2 len(len = 4
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
    
    
    

