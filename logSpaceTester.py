import math

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

xPrime = math.log(.2)
yPrime = math.log(.3)

col = [xPrime, yPrime]#, aPrime, bPrime]
actual = [math.log(.4), math.log(.6)]
actual2 = [math.log(.1), math.log(.9)]

col = normalizeColLog(col)
actual = normalizeColLog(actual2)


print col
print actual

