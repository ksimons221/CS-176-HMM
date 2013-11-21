from main import mainRunner

initialProbabilities = [0.603154, 0.357419, 0.0388879, 0.000539295]

converstionTable = [0.3225476896193923, 1.7457611011583467, 4.5366202969211304, 9.40]


transitionProbalities = [
[0.999916, 0.0000760902, 8.27877e-6, 1.14809e-7],
[0.000128404, 0.999786, 0.0000848889,    1.17723e-6],
[0.000128404, 0.000780214, 0.999068, 0.0000235507],
[0.000128404, 0.000780214, 0.00169821, 0.997393]
]

emissionI =   [0.999217, 0.996674, 0.991725, 0.983241]
emissionD =  [0.000782947, 0.00332648, 0.00827535, 0.0167592]
        
inputFileName = "sequences_2mu.fasta"


mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, "2mu")
