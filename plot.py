"""
Plotting file.
"""
import numpy as np
import matplotlib.pyplot as plt
import argparse
from matplotlib.pyplot import *

def plot_vert(a, b, c, d):
    t = range(len(a))
    plot(t, a, label='Viterbi decoding')
    plot(t, b, label='Posterior decoding')
    plot(t, c, label='Posterior mean')
    plot(t, d, label='True')

    legend()
    xlabel('locus')
    ylabel('TMRCA')
    grid(True)
    show()

def main():
    parser = argparse.ArgumentParser(description='Plots.')
    parser.add_argument('input_file')
    parser.add_argument('true_input_file')

    args = parser.parse_args()

    true_data = []
    with open(args.true_input_file) as f:
        true_data = [float(line.rstrip()) for line in f.readlines()]

    with open(args.input_file, 'r') as f:
        datum = [line.rstrip() for line in f.readlines()]
        a, b, c = [], [], []
        for i in range(1, len(datum)):
            d, e, f = datum[i].split()
            a.extend([float(d)])
            b.extend([float(e)])
            c.extend([float(f)])
        plot_vert(a,b,c,true_data)
        f.close()


if __name__ == '__main__':
    main()

