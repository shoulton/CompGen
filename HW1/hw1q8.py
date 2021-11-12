# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:46:03 2021

@author: Sarah
"""

import sys

def collapse(sequence):
    currLet = ''
    collapsed = ''
    
    for letter in sequence:
        if letter != currLet:
            collapsed = collapsed + letter
            currLet = letter
    return collapsed

def oneMistake(t, p):
    mistakes = 0
    
    for i in range(len(t)):
        tLet = t[i]
        pLet = p[i]
        
        if tLet != pLet:
            if mistakes == 1:
                return False
            if mistakes == 0:
                mistakes = 1
            
    return True

if __name__ == "__main__":

    t = sys.stdin.readline()
    p = sys.stdin.readline()
    
    collapsed = collapse(t)
   
    indices = []
    
    for i in range(len(collapsed) - len(p) + 1):
        subseq = collapsed[i:i+len(p) - 1]
        if oneMistake(subseq, p):
            indices.append(str(i))

    sys.stdout.write(' '.join(indices))