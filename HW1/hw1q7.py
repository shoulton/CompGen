# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:45:50 2021

@author: Sarah
"""

import sys
import itertools

def findAllSubseq(n):
    subseqs = {''}
    bases = 'ACGT'
    for i in range(n + 1):
        combos = set(itertools.combinations_with_replacement(bases, i))
        for combo in combos:
            combos = combos | (set(itertools.permutations(combo)))
        subseqs = subseqs | combos    
    return subseqs

def findComplement(subseq):
    ntDict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    
    suffix = ''
    
    for letter in subseq:
        suffix = suffix + ntDict[letter]
        
    return suffix[::-1]
    

if __name__ == "__main__":
   
    n = int(sys.stdin.readline().strip())
    n = int(n / 2)
    
    subseqs = findAllSubseq(n)
    palindromes = []
    for seq in subseqs:
        strSeq = ''.join(seq)
        if strSeq != '':
            fullPal = strSeq + findComplement(strSeq)
            palindromes.append(fullPal)
        
    
    sys.stdout.write('\n'.join(sorted(palindromes)) + '\n')