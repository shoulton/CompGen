# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 17:49:14 2021

@author: Sarah
"""

import sys

seq = ''

for ln in sys.stdin:
    for c in ln:
        if c in 'ACTG':
            seq = seq + c
            
allSubseq = {''}
repeatedSubseq = []

for i in range(len(seq)):
    subseq = seq[i:i+6]
    
    if subseq in allSubseq:
        repeatedSubseq.append(subseq)
    
    allSubseq.add(subseq)
        
sys.stdout.write(', '.join(sorted(repeatedSubseq)) + '\n') 