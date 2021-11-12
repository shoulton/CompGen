import sys

# taken from lecture code
def suffixArray(s):
    satups = sorted([(s[i:], i) for i in range(len(s))])
    return map(lambda x: x[1], satups)

# taken from lecture code
def bwtViaSa(t):
    # Given T, returns BWT(T) by way of the suffix array
    bw = []
    for si in suffixArray(t):
        if si == 0:
            bw.append('$')
        else:
            bw.append(t[si-1])
    return ''.join(bw) # return string-ized version of list bw

def bwtRuns(bwt):
    runs = []
    run = ""

    currChar = ''
    for char in bwt:
        if char is currChar:
            run += char
        if (char is not currChar) and (currChar is not ''):
            runs.append(run)
            run = char
            currChar = char
        if currChar is '':
            run = char
            currChar = char
    runs.append(run)
    return runs

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    seq = ""

    with open(infile, 'r') as fh:
        seq = fh.read().strip()
        fh.close()

    BWT = bwtViaSa(seq)
    runs = bwtRuns(BWT)
    outputString = BWT + " " + str(len(runs))
    with open(outfile, 'w') as of:
        of.write(outputString)
        of.close()