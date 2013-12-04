#!/bin/python
from sys import argv
from read_files import *
def correlation(vec1,vec2):
    size1 = reduce(lambda x,y:x+y,vec1)
    size2 = reduce(lambda x,y:x+y,vec2)

    return reduce(lambda x,y:x+y, [min(float(vec1[i])/size1,float(vec2[i])/size2) for i in range(len(vec1))])



def main():

    f1 = "transfers/TRANSH3K23ac.wip"
    f2 = "transfers/TRANSH3K18ac.wip"

    if(len(argv)>1):
        f1 = argv[1]
        f2 = argv[2]

    vec1,vec2 = GetAll(f1,f2)

    print "Correlation is: ",correlation(vec1,vec2)

if __name__ == "__main__":
    main()
