# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 16:41:06 2021

@author: Sarah
"""
import sys

seq = sys.stdin.readline().strip()
pattern = sys.stdin.readline().strip()


patLen = len(pattern)

splits = [seq[i:i+patLen] for i in range(0, (len(seq) - patLen + 1))]


count = 0

for split in splits:
    if split == pattern:
        count = count + 1

sys.stdout.write(str(count))