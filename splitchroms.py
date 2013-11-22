#!/bin/python

from sys import argv


def splitchroms(filename):
    print "splitting: "+filename
    fp = open(filename)

    namepref = filename[:filename.rfind(".wig")]+"_"


    name = namepref+"chr1"+".wig"
    chrom = "chr1"

    ofp = open(name,"w")
    print "writing to "+name
    for line in fp:
        s = line.find("chrom=")
        if(s!=-1):
            newchrom = line[s:].split()[0].split("=")[1]
            if(newchrom !=chrom):
                print line
                ofp.close()
                chrom = line.split()[1].split("=")[1]
                name = namepref+chrom +".wig"
                print "writing to "+name
                ofp = open(name,"w")
        ofp.write(line)
    ofp.close()
    fp.close()

if __name__=="__main__":
    splitchroms(argv[1])
