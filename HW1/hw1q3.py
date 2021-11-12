# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 15:49:16 2021

@author: Sarah
"""

import sys

output = []

proteinDict = {'UUU':'F', 'UUC':'F', 'UUA':'L', 'UUG':'L','CUU':'L','CUC':'L',
               'CUA':'L','CUG':'L','AUU':'I','AUC':'I','AUA':'I','AUG':'M',
               'GUU':'V','GUC':'V','GUA':'V','GUG':'V','UCU':'S','UCC':'S',
               'UCA':'S', 'UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
               'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A','GCC':'A',
               'GCA':'A','GCG':'A','UAU':'Y','UAC':'Y','CAU':'H','CAC':'H',
               'CAA':'Q','CAG':'Q','AAU':'N','AAC':'N','AAA':'K','AAG':'K',
               'GAU':'D','GAC':'D','GAA':'E','GAG':'E','UGU':'C','UGC':'C',
               'UGG':'W','CGU':'R','CGC':'R','CGA':'R','CGG':'R','AGU':'S',
               'AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G','GGA':'G',
               'GGG':'G'}

seq = ''
for ln in sys.stdin:
    for c in ln:
        if c in 'ACUG':
            seq = seq + c
            
trios = [seq[i:i+3] for i in range(0, len(seq), 3)]       
for trio in trios:
    if trio in proteinDict:
        output.append(proteinDict[trio])
            
sys.stdout.write(''.join(output) + '\n') 