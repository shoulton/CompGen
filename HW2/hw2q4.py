import sys
from collections import OrderedDict
# adapted from jupyter notebook referenced in homework
def phred33_to_q(qual):
  """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
  qualities = []
  for q in qual:
      qualities.append(ord(q)-33)
  return qualities

def parse_fastq(filename):

    seqs = []
    qualities = []
    with open(filename, 'r') as fh:
        first_line = fh.readline()
        while len(first_line) > 0:
            name = first_line[1:].rstrip()
            seq = fh.readline().rstrip()
            fh.readline()  # ignore line starting with +
            qual = fh.readline().rstrip()
            seqs.append(seq)
            qualities.append(qual)
            first_line = fh.readline()

    quals = [phred33_to_q(x) for x in qualities]
    return seqs, quals

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

def approximateMatch(genome, pattern, index, maxMismatch):

    if (index + len(pattern)) > len(genome):
        return False, 0

    mismatches = 0

    genomeShort = genome[index:]

    for i in range(len(pattern)):
        patChar = pattern[i]
        genomeChar = genome[index + i]
        if patChar is not genomeChar:
            mismatches += 1
        if mismatches > maxMismatch:
            return False, 0
    return (mismatches <= maxMismatch), mismatches

def getAllMatches(reads, kmers):

    allMatchesPerRead = {}
    for i in range(len(reads)):
        read = reads[i]

        partitions = [read[0:5], read[5:10], read[10:15], read[15:20]]
        partitionOffset = [0, 5, 10, 15]
        matches = {0:[], 1:[], 2:[], 3:[]}
        readMatches = []
        for j in range(len(partitions)):
            offset = partitionOffset[j]
            partition = partitions[j]

            if partition not in kmers:
                readMatches.append(0)

            if partition in kmers:
                readMatches.append(len(kmers[partition]))
                for index in kmers[partition]:
                    genomeIndex = index - offset
                    if genomeIndex >= 0:
                        match, mismatches = approximateMatch(genome, read, genomeIndex, 3)
                        if match:
                            matches[mismatches].append(genomeIndex)

        matches[0] = set(matches[0])
        matches[1] = set(matches[1])
        matches[2] = set(matches[2])
        matches[3] = set(matches[3])

        allMatches = matches[0] | matches[1] | matches[2] | matches[3]
        for m in allMatches:
            if m in allMatchesPerRead:
                allMatchesPerRead[m].append(i)
            else:
                allMatchesPerRead[m] = [i]
    return allMatchesPerRead

def getCharAndQual(reads, qualities, genome):
    res = {}
    for offset in allMatchesPerRead:
        matching = allMatchesPerRead[offset]
        for i in range(len(matching)):
            read = reads[matching[i]]
            quality = qualities[matching[i]]
            for j in range(len(read)):
                readChar = read[j]
                readQual = quality[j]
                genomeIndex = offset + j
                genomeChar = genome[genomeIndex]
                if genomeIndex not in res:
                    res[genomeIndex] = [[readChar, readQual]]
                else:
                    res[genomeIndex].append([readChar, readQual])
    return res

def findGreatestWeight(baseDict, refBase):
    greatBase = '-'
    secondBase = '-'
    greatWeight = 0
    secondWeight = 0
    for base in baseDict.keys():
        if base is not refBase:
            weight = baseDict[base]
            if weight > greatWeight:
                secondBase = greatBase
                secondWeight = greatWeight
                greatWeight = weight
                greatBase = base
            if weight == greatWeight:
                if base < greatBase:
                    secondBase = greatBase
                    secondWeight = greatWeight
                    greatBase = base
                    greatWeight = weight
                if base > greatBase:
                    if weight >= secondWeight:
                        if base < secondBase:
                            secondBase = base
                            secondWeight = weight
    return greatBase, greatWeight, secondBase, secondWeight

if __name__ == "__main__":

    fasta = sys.argv[1]
    fastq = sys.argv[2]
    outfile = sys.argv[3]

    genome = parse_fasta(fasta)
    genome = "".join(genome.split())

    reads, qualities = parse_fastq(fastq)

    kmers = kmer(5, genome)

    file = ""

    allMatchesPerRead = getAllMatches(reads, kmers)

    indexDict = getCharAndQual(reads, qualities, genome)
    indexDict = OrderedDict(sorted(indexDict.items()))

    for index in indexDict.keys():
        refBase = genome[index]
        possibles = indexDict[index]
        totalWeights = {}
        for possible in possibles:
            base = possible[0]
            qual = possible[1]
            if base is not refBase:
                if base in totalWeights:
                    totalWeights[base] += qual
                else:
                    totalWeights[base] = qual
        for nonRefBase in totalWeights.keys():
            if nonRefBase is not refBase and totalWeights[nonRefBase] > 20:
                baseOffset = index
                firstBase, firstWeight, secondBase, secondWeight = findGreatestWeight(totalWeights, refBase)
                file += str(baseOffset) + " " + str(refBase) + " " + firstBase + " " + str(firstWeight) + " " + secondBase + " " + str(secondWeight) + "\n"

    with open(outfile, 'w') as out:
        out.write(file)
