import numpy as np
import sys
from math import sqrt

def makevector(filename,chromname="all"):
    fp = open(filename)

    vec = []
    pos = 1
    for line in fp:
        data = line.split()
        if(data[0] != chromname and chromname != "all"):
            continue
        while(int(data[1])!=pos):
            vec.append(0)
            pos+=1000
        vec.append(int(data[2]))
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


def Pad(vec1,vec2):
    if(len(vec1)>len(vec2)):
        vec2+=[0.0]*(len(vec1)-len(vec2))
    if(len(vec2)>len(vec1)):
        vec1+=[0.0]*(len(vec2)-len(vec1))
    return (vec1,vec2)

