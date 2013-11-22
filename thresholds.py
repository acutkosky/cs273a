#!/bin/python
import heapq as h

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def findthresh(filename,ratio=0.02):
    if(ratio<0):
        return -1
    upperbound = int(round(file_len(filename)*ratio))
    fp = open(filename)
    count = 0
    tops = [0]*upperbound
    h.heapify(tops)
    for line in fp:
        try:
            h.heappushpop(tops,int(line))
            count += 1
        except:
            pass
    fp.close()
    print "file: ",filename," thresh: ",tops[0]
    return tops[0]-0.05


