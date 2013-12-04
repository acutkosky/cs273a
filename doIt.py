#!/usr/local/bin/python
import sys
import read_files
import spectralClustering
import linearRegression
from random import choice

def main():
    if len(sys.argv) != 3:
        print "Usage: %s <csv file containing correlation matrix> <num. clusters>\n" %(sys.argv[0])
        sys.exit(-1)
    fileName = sys.argv[1]
    numClusters = int(sys.argv[2])
    (contents, fileList) = spectralClustering.readFile(fileName, "\t")

    fileList = spectralClustering.runClustering(contents, fileList, numClusters)

    for clusterFiles in fileList:
        print "Cluster files:"
        print clusterFiles
        if len(clusterFiles) <= 1:
            continue

        pref = "transfers/TRANS"
        training = clusterFiles[:]
        training = [pref + x for x in training]
        test = choice(training)
        training.remove(test)
        X = read_files.GetMatrix(training, "chr1")
        Y = read_files.makevector(test, "chr1")

        if len(Y) > len(X):
            Y = Y[:len(X)]
        elif len(Y) < len(X):
            Y = Y + [0]*(len(X)-len(Y))

        assert (len(X) == len(Y))

        clf = linearRegression.linearRegression(X,Y)
        score = clf.score(X,Y)
        print "Predicting "+test[len(pref):-len(".wip")]
        print "Linear regression R^2 score: %f" %(score)
        print "Linear regression RMS error: %f" %(read_files.RMSerror(clf,X,Y))
        print "Linear regression coefficients:"
        print clf.coef_

main()
