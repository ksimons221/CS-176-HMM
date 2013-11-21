from main import mainRunner

initialProbabilities = [0.603154, 0.357419, 0.0388879, 0.000539295]

converstionTable = [0.3225476896193923, 1.7457611011583467, 4.5366202969211304, 9.40]


transitionProbalities = [
[0.999916, 0.0000760902, 8.27877e-6, 1.14809e-7],
[0.000128404, 0.999786, 0.0000848889,    1.17723e-6],
[0.000128404, 0.000780214, 0.999068, 0.0000235507],
[0.000128404, 0.000780214, 0.00169821, 0.997393]
]

emissionI =   [0.998046, 0.99173, 0.979578, 0.959163]
emissionD =  [0.00195405, 0.00826963, 0.0204217, 0.040837]
        
inputFileName = "sequences_5mu.fasta"


mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, "5mu")
