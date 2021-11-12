import sys

def write_solution(unitigID, unitigSequence, n, out_fh, per_line=60):
    offset = 0
    out_fh.write(f">{unitigID} {n}\n")
    while offset < len(unitigSequence):
        line = unitigSequence[offset:offset + per_line]
        offset += per_line
        out_fh.write(line + "\n")


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

if __name__ == "__main__":
    fastqFile = sys.argv[1]
    unitigs = sys.argv[2]
    outfile = sys.argv[3]

    seqDict = parse_fastq(fastqFile)

    firstunitig = True
    with open(unitigs, "r") as unitigFh:
        line = unitigFh.readline()
        unitigId = ""
        numUnitig = 0
        unitigSeq = ""
        while line:
            splits = line.split()
            if len(splits) == 1:
                if numUnitig > 0:
                    if firstunitig is False:
                        with open(outfile, "a") as outfh:
                            #print(len(unitigSeq))
                            write_solution(unitigId, unitigSeq, numUnitig, outfh)
                            outfh.close()
                    if firstunitig is True:
                        with open(outfile, "w") as outfh:
                            #print(len(unitigSeq))
                            write_solution(unitigId, unitigSeq, numUnitig, outfh)
                            outfh.close()
                        firstunitig = False
                unitigId = splits[0]
                numUnitig = 1
                unitigSeq = seqDict[unitigId]
            if len(splits) == 2:
                numUnitig += 1
                unitigSeq += seqDict[splits[1]][int(splits[0]):]
            line = unitigFh.readline()
        unitigFh.close()

    if numUnitig > 0:
        with open(outfile, "a") as outfh:
            #print(len(unitigSeq))
            write_solution(unitigId, unitigSeq, numUnitig, outfh)
            outfh.close()




