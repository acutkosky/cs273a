#!/usr/local/bin/python
import numpy as np
import sklearn
import csv
import sys
from sklearn.cluster import spectral_clustering

def readFile(f, delim=" ",hack=False):
    retArray = []
    fHandle = open(f, "r")
    line = fHandle.readline()
    fileList = line.split()
    csvReader = csv.reader(fHandle, delimiter=delim)
    for row in csvReader:
        if len(row) > 0:
            if(hack):
                retArray.append([float(x) for x in row[:-1]])
            else:
                retArray.append([float(x) for x in row])                
    return (retArray, fileList)


def runClustering(contents, fileList, numClusters):
    print contents[0]
    data = np.array(contents)
    print data.shape
    print data[0]
    labels = spectral_clustering(data, numClusters)
#    print labels
#    print "Length: %d" %(len(labels))
    returnList = []
    for cluster in range(numClusters):
        clusterContents = filter(lambda x:labels[x] == cluster,range(len(labels)))
        clusterFiles = [fileList[i] for i in clusterContents]
        returnList.append(clusterFiles)

    return returnList
