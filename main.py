
cluster = []
with open("project_result.txt",'r') as file :
    for line in file :
        cluster.append(line.strip('\n').split(' '))

Gtcluster = []
with open("complex_merged.txt", 'r') as file :
    for line in file :
        Gtcluster.append(line.strip('\n').split(' '))
Gtclusters = []
for n in range(len(Gtcluster)) :
    Gtclusters.append(Gtcluster[n][1:])
#print(cluster[0])
print(Gtclusters[0][0])

if(cluster[0][1] == Gtclusters[570][0]) :
    print(1)
else :
    print(0)

fscores = []
x = 0
y = 0
'''
for i in range(len(cluster)) :
    for j in range(len(cluster[i])) :
        for k in range(len(Gtclusters)) :
            for l in range(len(Gtclusters[k])) :
                i = 0
'''

def precision(cluster, Gtcluster) :
    for i in range(len(cluster)) :
        return


def recall(cluster, Gtcluster) :
    return

def fscore(precision, recall) :
    sums = precision + recall
    multis = precision * recall
    calc1 = multis / sums
    result = calc1 * 2
    return result