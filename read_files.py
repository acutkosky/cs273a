import numpy as np
import sys
from math import sqrt

def makevector(filename,chromname):
    fp = open(filename)

    vec = []
    pos = 1
    lineNum = 0
    prevChr = ""
    curChr = ""
    for line in fp:
        lineNum += 1
        data = line.split()
        if(data[0] != chromname):
            continue
#        if (curChr != data[0]):
#            pos = 1
#            curChr = data[0]
#            print "Entering chromosome %s" %(curChr)

        while(int(data[1])!=pos):
            vec.append(0)
            pos+=1000
        vec.append(int(data[2]))
#        if lineNum % 10000 == 0:
#            print "Line %d" %(lineNum)
    print "done"
    return vec



def GetMatrix(filenames,chromname):
    print filenames
    temp = [makevector(filename,chromname) for filename in filenames]
    m = max([len(x) for x in temp])
    temp = [x + [0]*(m-len(x)) for x in temp]
    return np.transpose(np.array(temp))


def RMSerror(clf,X,Y):
    mse = 0.0
    for i in range(len(X)):
        mse += (clf.predict(X[i])-Y[i])**2
    return sqrt(mse/len(X))


def GetAll(file1,file2):
    chroms = ["chr"+str(x) for x in range(1,23)]+["chrX","chrY","chrM"]
    vec1 = []
    vec2 = []
    for chrom in chroms:
        v1,v2 = Pad(makevector(file1,chrom),makevector(file2,chrom))
        vec1 += v1
        vec2 += v2
    return vec1,vec2

def Pad(vec1,vec2):
    if(len(vec1)>len(vec2)):
        vec2+=[0.0]*(len(vec1)-len(vec2))
    if(len(vec2)>len(vec1)):
        vec1+=[0.0]*(len(vec2)-len(vec1))
    return (vec1,vec2)

