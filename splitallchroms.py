#!/bin/python

from os import walk,path
from sys import argv
from splitchroms import splitchroms

def traverse(directory):
    for root,dirs,files in walk(directory):
        for f in files:
            splitchroms(path.join(root,f))



if __name__=="__main__":
    traverse(argv[1])
