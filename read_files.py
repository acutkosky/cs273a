import numpy as np
import sys

def makevector(filename,chromname):
    fp = open(filename)

    vec = []
    pos = 1
    for line in fp:
        data = line.split()
        if(data[0] != chromname):
            continue
        while(int(data[1])!=pos):
            vec.append(0)
            pos+=1000
        vec.append(int(data[2]))
    return vec



def GetMatrix(filenames,chromname):
    print filenames
    temp = [makevector(filename,chromname) for filename in filenames]
    m = max([len(x) for x in temp])
    temp = [x + [0]*(m-len(x)) for x in temp]
    return np.transpose(np.array(temp))
