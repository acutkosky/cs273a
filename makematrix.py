from read_files import GetAll
from correlation import correlation
filenames = ["H2A.Z.wip", "H2BK15ac.wip", "H3K18ac.wip", "H3K27me3.wip", "H3K4me3.wip", "H3K9ac.wip", "H4K8ac.wip", "H2AK5ac.wip", "H2BK20ac.wip", "H3K23ac.wip", "H3K36me3.wip", "H3K56ac.wip", "H3K9me3.wip", "H4K91ac.wip", "H2BK120ac.wip", "H2BK5ac.wip", "H3K23me2.wip", "H3K4ac.wip", "H3K79me1.wip", "H4K20me1.wip", "H2BK12ac.wip", "H3K14ac.wip", "H3K27ac.wip", "H3K4me2.wip", "H3K79me2.wip", "H4K5ac.wip"]


matrix = [[0.0]*len(filenames) for i in range(len(filenames))]
pref = "H1NonBinTSVs/TRANS2"

f = open("NonBinH1CorMatTSV","w")

f.write(reduce(lambda x,y:x+"\t"+y,filenames))
count = 0.0
for i in range(len(filenames)):
    for j in range(i,len(filenames)):
        count += 1.0
        print "Percent Done: %f%%" %(100.0*count/(len(filenames)*(len(filenames)+1)/2.0))
        print "correlating: %s with %s" %(filenames[i],filenames[j])
        f1 = pref+filenames[i]
        f2 = pref+filenames[j]
        vec1,vec2 = GetAll(f1,f2)
        matrix[i][j] = correlation(vec1,vec2)
        matrix[j][i] = matrix[i][j]
        print "answer: %f" % (matrix[i][j])
        

for i in range(len(filenames)):
    f.write(reduce(lambda x,y:str(x)+"\t"+str(y),matrix[i]))


        
            
