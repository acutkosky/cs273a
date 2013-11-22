#!/bin/python

from os import walk,path
from sys import argv
from splitchroms import splitchroms

def traverse(directory):
    rs = set([])
    for root,dirs,files in walk(directory):
        for f in files:
            if(root not in rs):
                if(root.find("Histone")!=-1):
                    if(root.find("H3K4me1") == -1):
                        if(len(f.split("_"))==2):
                            if(f.find("_chr1")!=-1):
                                rs.add(root)
                                print path.join(root,f)



if __name__=="__main__":
    traverse(argv[1])
