from main import mainRunner

initialProbabilities = [0.603154, 0.357419, 0.0388879, 0.000539295]

converstionTable = [0.3225476896193923, 1.7457611011583467, 4.5366202969211304, 9.40]


transitionProbalities = [
[0.999916, 0.0000760902, 8.27877e-6, 1.14809e-7],
[0.000128404, 0.999786, 0.0000848889,    1.17723e-6],
[0.000128404, 0.000780214, 0.999068, 0.0000235507],
[0.000128404, 0.000780214, 0.00169821, 0.997393]
]

emissionI =   [0.999608, 0.998334, 0.995844, 0.991548]
emissionD =  [0.000391695, 0.00166636, 0.00415567, 0.008452]
        
inputFileName = "sequences_mu.fasta"


mainRunner(inputFileName, initialProbabilities, transitionProbalities, emissionI, emissionD, converstionTable, "mu", "initial_param")
