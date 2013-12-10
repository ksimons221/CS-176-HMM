"""
Plotting file.
"""
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Plots.')
    parser.add_argument('input_file')

    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        datum = [line.rstrip() for line in f.readlines()]
        f.close()
    

if __name__ == '__main__':
    main()

t = arange(0.0, 2.0, 0.01)
s = sin(2*pi*t)
plot(t, s)

xlabel('time (s)')
ylabel('voltage (mV)')
title('About as simple as it gets, folks')
grid(True)
savefig("test.png")
show()