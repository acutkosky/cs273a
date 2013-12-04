#!/bin/python

def correlation(vec1,vec2):
    size1 = reduce(lambda x,y:x+y,vec1)
    size2 = reduce(lambda x,y:x+y,vec2)

    return reduce(lambda x,y:x+y, [min(float(vec1[i])/size1,float(vec2[i])/size2) for i in range(len(vec1))])


from read_files import *

vec1,vec2 = Pad(makevector("transfers/TRANSH3K23ac.wip","all"),makevector("transfers/TRANSH3K18ac.wip","all"))

print "Correlation is: ",correlation(vec1,vec2)
