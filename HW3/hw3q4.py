import random

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

def mutate(x, n):
    y = x[:] # y = a copy of x
    for _ in range(n):
        # pick a random position in the string
        randompos = random.randint(0, len(x)-1)
        # replace with a random base: A, C, G or T
        y[randompos] = random.choice("ACGT")
    return y

if __name__ == "__main__":
    x = 'ACTGAG'
    y = mutate(x, 3)
    print(str(edDistDp(x, y, 1, 1)))