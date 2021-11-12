# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 18:18:02 2021

@author: Sarah
"""

import sys
from io import StringIO
#from Bio import SeqIO

# adapted from jupyter notebook in homework
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

# pulled from jupyter notebook referenced in homework
def phred33_to_q(qual):
  """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
  return ord(qual)-33

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]

    sequences, qualities = parse_fastq(infile)

    #reads = list(SeqIO.parse(infile, "fastq"))
    #sequences = [x.seq for x in reads]
    #qualities = [x.letter_annotations['phred_quality'] for x in reads]


    minmax = []
    for i in range(len(sequences[0])):
        min = 1000
        max = -10
        for quality in qualities:
            q = quality[i]
            q = phred33_to_q(q)
            if q > max:
                max = q
            if q < min:
                min = q
        minmax.append((min, max))

    out = open(outfile, 'w')
    for pair in minmax:
        out.write(str(pair[0]) + ' ' + str(pair[1]) + '\n')
