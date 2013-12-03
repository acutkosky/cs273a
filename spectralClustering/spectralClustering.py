#!/usr/local/bin/python
import numpy as np
import sklearn
import csv
import sys
from sklearn.cluster import spectral_clustering

def readFile(f, delim=" "):
    retArray = []
    fHandle = open(f, "r")
    fHandle.readline()
    csvReader = csv.reader(fHandle, delimiter=delim)
    for row in csvReader:
        if len(row) > 0:
            print row
            retArray.append([float(x) for x in row[:-1]])
    return retArray


def main():
    if len(sys.argv) != 3:
        print "Usage: %s <csv file containing correlation matrix> <num. clusters>\n" %(sys.argv[0])
        sys.exit(-1)

    fileName = sys.argv[1]
    numClusters = int(sys.argv[2])
    contents = readFile(fileName, "\t")
    print contents

    data = np.array(contents)
    labels = spectral_clustering(data, numClusters)
    print labels
    print "Length: %d" %(len(labels))


main()
