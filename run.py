"""
Simple execution file.
"""
import argparse
from mainForEM import mainRunnerEM
from main import mainRunner
from ForwardAlgorithm import calculateForwardAlgoLog, likelihoodOfSequence
from BackwardsAlgorithm import calculateBackwardsAlgoLog
from Viterbi import hiddenStatePath, getLastState, calculateVeterbiEncodingLog
from EM import calculateBigVars, calculateNewInitialValues
from helperFunctions import computePosteriorDecodingLog, calculatePosteriorMeanLog

conversion_table = [0.3225476896193923, 1.7457611011583467, 4.5366202969211304, 9.40]

def read_file(input_file):
    f = open(input_file, 'r')
    sequences = []

    for line in f:
        line = line.rstrip()
        if line[0] == '>':
            sequences.append('')
        else:
            sequences[-1] += line
    return sequences

def write_estimated_parameters(params):
    output = []

    output.extend('# Marginal probabilities\n')
    for i in range(4):
        output.extend('{0}\n'.format(params['m'][i]))
    output.extend('\n')

    output.extend('# Transition Probabilities\n')
    for i in range(4):
        for j in range(4):
            output.extend('{0} '.format(params['t'][i][j]))
        output.extend('\n')
    output.extend('\n')

    output.extend('# Emission Probabilities\n')
    for i in range(4):
        output.extend('{0} {1}\n'.format(params['e']['i'][i], params['e']['d'][i]))

    return ''.join(output)

def write_likelihoods(initial_likelihood, estimated_likelihood):
    output = []

    output.extend('# Likelihood under {initial, estimated} parameters\n')
    output.extend('{0}\n'.format(initial_likelihood))
    output.extend('{0}'.format(estimated_likelihood))

    return ''.join(output)

def expectation_maximization(sequences, params):
    forward_table = calculateForwardAlgoLog(params['m'], params['t'], params['e']['i'], params['e']['d'], sequences)
    likelihood = likelihoodOfSequence(forward_table)
    backward_table = calculateBackwardsAlgoLog(params['t'], params['e']['i'], params['e']['d'], sequences)
    posterior_table_and_route_log = computePosteriorDecodingLog(forward_table, backward_table, len(sequences[0]), likelihood)
    check = calculateBigVars (posterior_table_and_route_log[0], sequences, forward_table, backward_table, params['t'], params['e']['i'], params['e']['d'], likelihood)
    results = calculateNewInitialValues(check) 
    params['m'] = results[0]
    params['t'] = results[1]
    params['e']['i'] = results[2]
    params['e']['d'] = results[3]
    return params, likelihood

def parse_params(input_file):
    f = open(input_file, 'r')
    lines = [line.rstrip() for line in f.readlines()]
    lines = [line for line in lines if len(line) != 0 and line[0] != '#']

    initial_probabilities = []
    for _ in range(4):
        initial_probabilities.append(float(lines.pop(0).split()[1]))

    transition_probabilities = []
    for _ in range(4):
        transition_probabilities.append([float(x) for x in lines.pop(0).split()])

    emissionI = []
    emissionD = []
    for _ in range(4):
        a, b, c = lines.pop(0).split()
        emissionI.append(float(b))
        emissionD.append(float(c))
    emissions = {'i': emissionI, 'd': emissionD}
    f.close()

    return {'m': initial_probabilities, 't': transition_probabilities, 'e': emissions}

def viterbi(sequences, params):
    decoding = []

    forward_table = calculateForwardAlgoLog(params['m'], params['t'], params['e']['i'], params['e']['d'], sequences)
    likelihood = likelihoodOfSequence(forward_table)
    backward_table = calculateBackwardsAlgoLog(params['t'], params['e']['i'], params['e']['d'], sequences)
    viterbi_encoding_log = calculateVeterbiEncodingLog(params['m'], params['t'], params['e']['i'], params['e']['d'], sequences)
    viterbi_states_log = hiddenStatePath(viterbi_encoding_log[1], len(sequences[0]), getLastState(viterbi_encoding_log[0], len(sequences[0])))
    posterior_table_and_route_log = computePosteriorDecodingLog(forward_table, backward_table, len(sequences[0]), likelihood)
    posterior_states_log = posterior_table_and_route_log[1]
    posterior_mean_log = calculatePosteriorMeanLog(posterior_table_and_route_log[0], len(sequences[0]), conversion_table)

    decoding.extend('# Viterbi_decoding posterior_decoding posterior_mean\n')
    for i in range(len(viterbi_states_log)):
        decoding.extend('{0} {1} {2}\n'.format(conversion_table[viterbi_states_log[i]], conversion_table[posterior_states_log[i]], posterior_mean_log[i]))

    return likelihood, ''.join(decoding)

def main():
    parser = argparse.ArgumentParser(description='Perform Hidden Markov Model Calculations.')

    parser.add_argument('input_FASTA_file', metavar='input_sequences', help='the input FASTA file')
    parser.add_argument('input_initial_parameters', metavar='input_parameters', help='the input initial parameters file')
    parser.add_argument('output_estimated_parameters')
    parser.add_argument('output_likelihoods')
    parser.add_argument('output_initial_decodings')
    parser.add_argument('output_estimated_decodings')

    args = parser.parse_args()

    sequences = read_file(args.input_FASTA_file)
    params = parse_params(args.input_initial_parameters)

    initial_likelihood, initial_decoding = viterbi(sequences, params)

    for _ in range(15):
        params, estimated_likelihood = expectation_maximization(sequences, params)

    estimated_decoding = viterbi(sequences, params)[1]
    
    with open(args.output_estimated_parameters, 'w') as f:
        f.write(write_estimated_parameters(params))
        f.close()

    with open(args.output_likelihoods, 'w') as f:
        f.write(write_likelihoods(initial_likelihood, estimated_likelihood))
        f.close()

    with open(args.output_initial_decodings, 'w') as f:
        f.write(initial_decoding)
        f.close()

    with open(args.output_estimated_decodings, 'w') as f:
        f.write(estimated_decoding)
        f.close()

if __name__ == '__main__':
    main()