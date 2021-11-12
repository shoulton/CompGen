# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 13:18:44 2021

@author: Sarah
"""

import sys

output = []
ntDict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

for ln in sys.stdin:
    for c in ln:
        if c in 'ACTG':
            output.append(ntDict[c])
            
sys.stdout.write(''.join(output) + '\n') 