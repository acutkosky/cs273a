

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



def GetVectors(filenames,chromname):
    return [makevector(filename,chromname) for filenam in filenames]


            

    
        
