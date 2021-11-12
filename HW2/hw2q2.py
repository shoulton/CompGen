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

def exactMatch(genome, pattern, index):

    if (index + len(pattern)) > len(genome):
        return False

    for i in range(4, len(pattern)):
        patChar = pattern[i]
        genomeChar = genome[index + i]
        if patChar is not genomeChar:
            return False
    return True


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
        totalHits = 0
        fruitless = 0
        matches = ""
        prefix = read[:5]
        if prefix in kmers:
            totalHits = len(kmers[prefix])
            for index in kmers[prefix]:
                match = exactMatch(genome, read, index)
                if match:
                    matches += str(index) + " "
                else:
                    fruitless += 1
        file += str(totalHits) + ' ' + str(fruitless) + ' ' + matches.strip() + "\n"

    with open(outfile, 'w') as out:
        out.write(file)
