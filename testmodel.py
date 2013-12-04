#!/bin/python
import sys
import read_files
import spectralClustering
from sklearn import linear_model
import numpy as np

def getmat(inputs,length,chrom):
    mat = []
    for i in range(len(inputs)):
        print "working on %s" %(inputs[i])
        vec = read_files.makevector(inputs[i],chrom)
        if(len(vec)<length):
            vec += [0.0]*(length-len(vec))
        elif(len(vec)>length):
            vec = vec[:length]
        mat.append(vec)
    mat = np.transpose(np.array(mat))
    return mat


    
def main():

    pref = "IMR90NonBinTSVs/TRANS2"
    test = pref+"H4K91ac"+".wig"

    coefs = [-0.08555987,  0.04224826,  0.30660155,  0.14207714,  0.09993307, -0.08755021,
  0.37018674 , 0.30653058 , 0.04945284,  0.09621078]
    intercept = -8.38136976009

    chrom = "chr1"

    inputs = ["H2A.Z","H2BK15ac","H3K18ac","H2AK5ac","H2BK20ac","H3K23ac","H2BK120ac","H3K4ac","H2BK12ac","H3K14ac"]
    inputs = [pref+x+".wig" for x in inputs]

    Y = read_files.makevector(test,chrom)
    length = len(Y)
    
    M = getmat(inputs,length,chrom)

    clf = linear_model.LinearRegression()

    clf.coef_ = np.array(coefs)
    clf.intercept_ = intercept

    score = clf.score(M,Y)

    print "score: %f" % (score)

main()
