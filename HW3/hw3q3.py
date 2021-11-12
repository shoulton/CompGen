import sys
from numpy import zeros

# taken from lecture code
def edDistDp(x, y, m, g):
    """ Calculate edit distance between sequences x and y using
        matrix dynamic programming.  Return distance. """
    D = zeros((len(x)+1, len(y)+1), dtype=int)
    D[0, 1:] = range(1, len(y)+1)
    D[1:, 0] = range(1, len(x)+1)
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            delt = m if x[i-1] != y[j-1] else 0
            D[i, j] = min(D[i-1, j-1]+delt, D[i-1, j]+g, D[i, j-1]+g)
    return D[len(x), len(y)]

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]

    with open(infile, 'r') as fh:
        X = fh.readline().strip()
        Y = fh.readline().strip()
        M = int(fh.readline().strip())
        G = int(fh.readline().strip())
        fh.close()

    with open(outfile, 'w') as of:
        of.write(str(edDistDp(X, Y, M, G)))
        of.close()