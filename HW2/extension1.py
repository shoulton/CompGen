import sys

def parse_fasta(filename):
    with open(filename, 'r') as fh:
        throwaway = fh.readline()
        seq = fh.read()
    return seq

def kmer(k, seq):
    kmers = {}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if kmer in kmers:
            kmers[kmer].append(i)
        else:
            kmers[kmer] = [i]
    return kmers


if __name__ == "__main__":

    alpha = "".join(parse_fasta("sarscov2_alpha.fa").split())
    delta = "".join(parse_fasta("sarscov2_delta.fa").split())
    wuhan = "".join(parse_fasta("sarscov2_wuhan.fa").split())

    alphaKmers = kmer(20, alpha)
    deltaKmers = kmer(20, delta)
    wuhanKmers = kmer(20, wuhan)

    setAlpha = set(alphaKmers.keys())
    setDelta = set(deltaKmers.keys())
    setWuhan = set(wuhanKmers.keys())

    alphaUnionWuhan = setAlpha | setWuhan
    alphaIntersectWuhan = setAlpha & setWuhan

    onlyDelta = setDelta.difference(alphaUnionWuhan)
    notDelta = alphaIntersectWuhan.difference(setDelta)
    print(onlyDelta)
    print(notDelta)
