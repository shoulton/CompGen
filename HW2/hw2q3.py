import sys

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
    return seqs, qualities

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


if __name__ == "__main__":

    fasta = sys.argv[1]
    fastq = sys.argv[2]
    outfile = sys.argv[3]

    genome = parse_fasta(fasta)
    genome = "".join(genome.split())

    reads, qualities = parse_fastq(fastq)

    kmers = kmer(5, genome)

    file = ""

    for read in reads:

        partitions = [read[0:5], read[5:10], read[10:15], read[15:20]]
        partitionOffset = [0, 5, 10, 15]
        matches = {0:[], 1:[], 2:[], 3:[]}
        readMatches = []
        for i in range(len(partitions)):
            offset = partitionOffset[i]
            partition = partitions[i]

            if partition not in kmers:
                readMatches.append(0)

            if partition in kmers:
                readMatches.append(len(kmers[partition]))
                for index in kmers[partition]:
                    genomeIndex = index - offset
                    if genomeIndex >= 0:
                        match, mismatches = approximateMatch(genome, read, genomeIndex, 3)
                        if match:
                            matches[mismatches].append(str(genomeIndex))

        matches[0] = sorted(list(set(matches[0])))
        matches[1] = sorted(list(set(matches[1])))
        matches[2] = sorted(list(set(matches[2])))
        matches[3] = sorted(list(set(matches[3])))
        firstHalf = str(readMatches[0]) + " " + str(readMatches[1]) + " " + str(readMatches[2]) + " " + str(readMatches[3]) + " "
        secondHalf =  "0:" + ",".join(matches[0]) + " 1:" + ",".join(matches[1]) + " 2:" + ",".join(matches[2]) + " 3:" + ",".join(matches[3])
        file += firstHalf + secondHalf + "\n"

    with open(outfile, 'w') as out:
        out.write(file)