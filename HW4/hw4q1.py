import sys

def make_kmer_table(seqs, k):

    """ Given read dictionary and integer k, return a dictionary that
    maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)
    return table

def make_id_table(kmerTable):
    idTable = {}
    for kmer in kmerTable.keys():
        ids = kmerTable[kmer]
        for id in ids:
            if id not in idTable:
                idTable[id] = set()
            idTable[id] = idTable[id] | ids
    return idTable

def suffix_prefix_match(str1, str2, min_overlap):

    if len(str2) < min_overlap:
        return 0
    str2_prefix = str2[:min_overlap]
    str1_pos = -1
    while True:
        str1_pos = str1.find(str2_prefix, str1_pos + 1)
        if str1_pos == -1:
            return 0
        str1_suffix = str1[str1_pos:]
        if str2.startswith(str1_suffix):
            return len(str1_suffix)


def parse_fastq(filename):

    seqDict = {}
    with open(filename, 'r') as fh:
        first_line = fh.readline()
        while len(first_line) > 0:
            name = first_line[1:].rstrip()
            seq = fh.readline().rstrip()
            fh.readline()  # ignore line starting with +
            qual = fh.readline().rstrip()
            seqDict[name] = seq
            first_line = fh.readline()
        fh.close()
    return seqDict

def findReads(seqDict, idDict, k):
    output = ""
    for id1 in seqDict.keys():
        if id1 in idDict:
            seq1 = seqDict[id1]
            matches = {}
            for id2 in idDict[id1]:
                if id2 is not id1:
                    seq2 = seqDict[id2]
                    overlap = suffix_prefix_match(seq1, seq2, k)
                    if overlap not in matches:
                        matches[overlap] = []
                    matches[overlap].append(id2)

            matchKeys = sorted(matches.keys())
            if matchKeys:
                longestLen = matchKeys[len(matchKeys) - 1]
                if len(matches[longestLen]) == 1 and longestLen >= k:
                    output += id1 + " " + str(longestLen) + " " + str(matches[longestLen][0]) + "\n"

    return output

if __name__ == "__main__":
    infile = sys.argv[1]
    k = int(sys.argv[2])
    outfile = sys.argv[3]

    seqDict = parse_fastq(infile)
    filtered = make_kmer_table(seqDict, k)
    idTable = make_id_table(filtered)
    out = findReads(seqDict, idTable, k)


    with open(outfile, 'w') as fh:
        fh.write(out)
        fh.close()