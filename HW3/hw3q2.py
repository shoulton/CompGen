import sys

def uncompress(compressed):
    noSpaces = compressed.replace(" ", "")
    char = ''
    num = 0

    uncompressed = ""
    for i in range(len(noSpaces)):
        if i%2 != 0:
            pass
        else:
            char = noSpaces[i]
            i += 1
            num = int(noSpaces[i])
            while num > 0:
                uncompressed += char
                num -= 1
    return uncompressed


# taken from lecture code
def reverseBwt(bw):
    ''' Make T from BWT(T) '''
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0 # start in first row
    t = '$' # start with rightmost character
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t # prepend to answer
        # jump to row that starts with c of same rank
        rowi = first[c][0] + ranks[rowi]
    return t

# taken from lecture code
def firstCol(tots):
    ''' Return map from character to the range of rows prefixed by
        the character. '''
    first = {}
    totc = 0
    for c, count in sorted(tots.items()):
        first[c] = (totc, totc + count)
        totc += count
    return first

# taken from lecture code
def rankBwt(bw):
    ''' Given BWT string bw, return parallel list of B-ranks.  Also
        returns tots: map from character to # times it appears. '''
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots:
            tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    compressedBWT = ""

    with open(infile, 'r') as fh:
        compressedBWT = fh.read().strip()
        fh.close()

    uncompressed = uncompress(compressedBWT)
    original = reverseBwt(uncompressed)

    with open(outfile, 'w') as of:
        of.write(original)
        of.close()