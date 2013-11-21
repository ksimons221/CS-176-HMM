from helperFunctions import generateEmissionValue

def calculateBackwardsAlgo(transitionProbalities, emissionI, emissionD, sequences ):
    
    results = [[1,1,1,1]]

    endLength = len(sequences[0])
    for t in range(1, endLength):
        currentCol = [0,0,0,0]
        for i in range(4):
            singleValue = 0
            for j in range(4):
                indexInSequence = endLength - t;
                emissionValue = generateEmissionValue(indexInSequence, j, sequences, emissionI, emissionD)
                singleValue = singleValue + (results[0][j]*transitionProbalities[i][j]*emissionValue)
            currentCol[i] = singleValue
        results.insert(0,currentCol)
            
    return results;