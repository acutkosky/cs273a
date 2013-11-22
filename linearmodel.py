#!/bin/python
from sys import argv,stdout
import numpy as np
import random
from math import sqrt
from thresholds import findthresh

alphastart = 0.01
threshold = 0.5

class Window:
    

    def __init__(self,filename,thresh = -1):
        self.filename = filename
        self.start = None
        self.vector = []
        self.nextstart = None
        self.threshold = thresh
        self.initialize()

    def initialize(self):
        self.fp = open(self.filename)

        line = self.fp.readline()
        while(line.find("start=") == -1):
            line = self.fp.readline()
        
            
        self.start = int(line[line.find("start="):].split()[0].split("=")[1])
        count=self.start
        while(True):
            line = self.fp.readline().strip()
            try:
                if(self.threshold == -1):
                    self.vector.append(int(line))
                else:
                    self.vector.append( 1 if int(line)>self.threshold else 0 )
                count+=20
            except:
                if(line.find("start") == -1):
                    break
                nextstart=int(line[line.find("start="):].split()[0].split("=")[1])
                if(nextstart != count):
#                    print "ha!",nextstart,count
                    break
                else:
#                    print "going!"
                    pass

        while(line.find("start=") == -1 and len(line) != 0):
            line = self.fp.readline()
        if(len(line)!=0):
            self.nextstart=int(line[line.find("start="):].split()[0].split("=")[1])
        else:
            self.nextstart = count
            self.fp.close()

    def Reset(self):
        if(not self.fp.closed):
            self.fp.close()
        self.start = None
        self.vector = []
        self.nextstart = None
        self.initialize()


    def increment(self):
        if(self.fp.closed):
            return 0
        self.vector = []
        self.start = self.nextstart
        count = self.start
        while(True):
            line = self.fp.readline().strip()
            try:
                if(self.threshold == -1):
                    self.vector.append(int(line))
                else:
                    self.vector.append( 1 if int(line)>self.threshold else 0 )
                count += 20
            except:
                if(line.find("start") == -1):
                    break
                nextstart=int(line[line.find("start="):].split()[0].split("=")[1])
                if(nextstart != count):
#                    print "ha!",nextstart,count
                    break

                


        while(line.find("start=") == -1):
            line = self.fp.readline()
            if(len(line)==0):
                self.nextstart = count
                self.fp.close()
                return 1
            
        self.nextstart=int(line[line.find("start="):].split()[0].split("=")[1])
        return 1

    def skipto(self,start,end):
        a = 0
        while(self.nextstart<=start or (start-self.start)/20>=len(self.vector)):
            if(not self.increment()):
                return 0
#        if(self.nextstart<=end):
#            return 0
        if((end-self.start)/20>len(self.vector)):
            return -1
        if(self.start>end):
            return 0
        return 1

    def getregion(self,start,end):
        assert( (end-start)<1000)
#        print "hehe"
        if(self.start>start):
            if(end<self.start):# or (end-self.start)/20>len(self.vector)):
                   return []
            else:
#                print (end-self.start)/20,self.start,self.nextstart,self.start+20*len(self.vector),end,start
                return (self.start-start)/20*[0]+self.vector[:(end-self.start)/20]
#        print "hoho"

        r = self.skipto(start,end)
        if(r == 0):
#            print "returning empty"
            return []
        if(r == -1):
#            print "lolo"
#            print "gee",self.start,start,self.nextstart,end,(start-self.start)/20,self.vector[(start-self.start)/20:]#+[0.0]*((end-self.start)/20-len(self.vector))
            return self.vector[(start-self.start)/20:]+[0.0]*((end-self.start)/20-len(self.vector))
        #print start,end,self.start,(start-self.start)/20,(end-self.start)/20,len(self.vector),self.nextstart
        #print self.vector[(start-self.start)/20:(end-self.start)/20]
#        print "wat"
#        print (start-self.start)/20,(end-self.start)/20,start,end,self.start

        return self.vector[(start-self.start)/20:(end-self.start)/20]
        

class Target:
    def __init__(self,filename,thresh=-1):
        self.filename = filename
        self.Position = None
        self.Value = None
        self.threshold = thresh
        self.initialize()


    def initialize(self):
        self.fp = open(self.filename)

        line = self.fp.readline()
        while(line.find("start=") == -1):
            line = self.fp.readline()
        
        while(line.find("start=") != -1):            
            start = int(line[line.find("start="):].split()[0].split("=")[1])
            line = self.fp.readline().strip()

        self.Position = start
        if(self.threshold == -1):
            self.Value = int(line)
        else:
            self.Value = 1 if int(line)>self.threshold else 0

    def Update(self):
        if(self.fp.closed):
            return -1
        line = self.fp.readline().strip()
        if(len(line) == 0):
            self.fp.close()
            return -1
        self.Position += 20
        while(line.find("start=") != -1):            
#            print "target inced!"
            self.Position = int(line[line.find("start="):].split()[0].split("=")[1])
            line = self.fp.readline().strip()
            if(len(line) == 0):
                self.fp.close()
                return -1
        if(self.threshold == -1):
            self.Value = int(line)
        else:
            self.Value = 1 if int(line)>self.threshold else 0

        return self.Position
    
    def Reset(self):
        self.Position = None
        self.Value = None
        if(not self.fp.closed):
            self.fp.close()
        self.initialize()


class Regression:
    
    def __init__(self,n,k):
        self.Vector = np.array([random.uniform(-1.0/(n*k),1.0/(n*k)) for x in range(n*k)])
        self.Constant = 0.0#random.random()
        self.alpha = alphastart
        self.n = n
        self.k = k

    def Update(self,Input,Output):
        test = self.Predict(Input)#np.dot(self.Vector,Input)+self.Constant
#round((np.dot(self.Vector,Input)+self.Constant)/(100000*len(Input)))
        er = (test - Output)**2
        #gradient descent... assuming I can calculate derivatives properly
        for i in range(len(self.Vector)):
            self.Vector[i] -= (self.alpha/2.0 *Input[i]*(test-Output))/len(Input)

        self.Constant -= self.alpha/2.0*(test-Output)/len(Input)
        

        #print test,Output,self.Vector,Input,self.Constant
#        print Output,Input[-5],Input
#        if(not abs(Output-Input[-5])<0.1):
#            print "whoops"
#            exit()

        if(str(test) == "nan"):
            exit()
        return er
    
    def Test(self,Input,Output):
        test = self.Predict(Input)#np.dot(self.Vector,Input)+self.Constant
# round((np.dot(self.Vector,Input)+self.Constant)/(100000.0*len(Input)))
        return (test-Output)**2
    def Predict(self,Input):
        return np.dot(self.Vector,Input)+self.Constant


def Test(regions,target,regression,windowsize = (20,20),numsamples=-1):
    er = 0.0
    count = 0 
    vec = np.zeros(len(regression.Vector))
    while(target.Update() != -1):
        if(count>numsamples and numsamples != -1):
            break
        count +=1
        if(count %1000 == 0):
            print count
        if(target.Position-windowsize[0]<0):
            continue
        flag = False
        j=0
        for i in range(len(regions)):
            region = regions[i].getregion(target.Position-windowsize[0],target.Position+windowsize[1])

            if(region == []):
                for l in range(regression.k):
                    vec[j] = 0.0
                    j+=1
            else:
                for val in region:
                    vec[j] = val
                    j+=1

        assert(j==len(regression.Vector))
        count += 1
        er += regression.Test(vec,target.Value)

    return sqrt(er/count)

            
def Train(regions,target,regression,windowsize = (20,20),numsamples=-1):

    er = 0.0
    vec = np.zeros(len(regression.Vector))
    count = 0
    badset = []
    tempset = []
    while(target.Update() != -1):
        if(count>numsamples and numsamples != -1):
            break
        count +=1
        if(count %1000 == 0):
            print count,len(badset)
        if(target.Position-windowsize[0]<0):
            continue
        flag = False
        j=0
        for i in range(len(regions)):
            try:
                pass
#                if(i%(len(regions)/10) == 0):
#                    stdout.write("...%0.1f" % (float(i)/len(regions)*100.0))
            except:
#                print "what"
                pass

            region = regions[i].getregion(target.Position-windowsize[0],target.Position+windowsize[1])

            if(region == []):
                for l in range(regression.k):
                    vec[j] = 0.0
                    j+=1
            else:
                assert(len(region) == regression.k)
                for val in region:
                    vec[j] = val
                    j+=1

 #       stdout.write("\n")

        assert(j==len(regression.Vector))
#        if(count %1000 == 0):
#            print "predict: ",regression.Predict(vec)," val: ",target.Value," er: ",regression.Test(vec,target.Value)


        z = regression.Update(vec,target.Value)

        if(z>500):
            badset.append((vec,target.Value))

        tempset = []
        if(count % 100 == 0):
            for pair in badset:
                z = regression.Update(pair[0],pair[1])
                if(z>500):
                    tempset.append(pair)
            badset = tempset
        
        er += z
            
#    print "er: ",er/numsamples
    return er


def IterateTrain(regions,target,regression,windowsize=(20,20),numiters=50,numsamples=100000):

    for i in range(numiters):
        print "running iteration: "+str(i)+" of "+str(numiters)

        str(Train(regions,target,regression,windowsize,numsamples))
        regression.alpha -= alphastart*1.0/(float(numiters)+20.0)
        for region in regions:
            region.Reset()
        target.Reset()

        for region in regions:
            region.Reset()
        target.Reset()

    er = Test(regions,target,regression,windowsize,numsamples)
    print "er: ",er
    return er


def Initialize(inputfilesfile,targetfile,windowsize = (20,20)):
    fp = open(inputfilesfile)
    lines = [x.strip() for x in fp.readlines()]
    fp.close()
    regions = []
    count = 0
    print "finding thresholds:",len(lines)
    for inputfile in lines:
        count += 1
        print count
        thresh = findthresh(inputfile,threshold)
        regions.append(Window(inputfile,thresh))
    thresh = findthresh(targetfile,threshold)
    target = Target(targetfile,thresh)


    
    return regions,target,Regression(len(lines),(windowsize[1])/20-(-windowsize[0])/20)



def main(args):
    windowsize = (100,100)
    regions,target,regression = Initialize(args[1],args[2],windowsize)

    er = IterateTrain(regions,target,regression,windowsize)

    print "final error: ",er
    print "vector: ",regression.Vector,regression.Constant
if __name__=="__main__":
    main(argv)



