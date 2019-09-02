
def getInfo(caminhoArquivo):
    f = open(caminhoArquivo,'r')
    edges=0
    demand=0
    icounter=0
    jcounter=0
    for linha in f:
        if(linha=="\n"):
            continue
        if(not demand):
            if("DIMENSION" in linha):
                dim=int(linha.split()[-1:][0])
                distm=[[0 for x in range(dim)] for y in range(dim)]
            if("VEHICLES" in linha):
                veic=int(linha.split()[-1:][0])
            if("CAPACITY" in linha):
                cap=int(linha.split()[-1:][0])
            if("DEMAND_SECTION" in linha):
                demand=True
                demandm=[]
                continue
        if(demand==True):
            if("EDGE_WEIGHT_SECTION" in linha):
                demand=False
                edges=True
                continue
            node,cost=linha.split()
            demandm.append([int(node),int(cost)])
        if(edges==True):
            jcounter=0
            for v in linha.split():
                distm[icounter][jcounter]=int(v)
                jcounter+=1
            icounter+=1
    return dim,veic,cap,demandm,distm

def isValid(caminho,demandm,cap):
    capcam=0
    for x in caminho:
        capcam+=demandm[int(x)][1]
    if(capcam>cap):
        return 0
    else:
        return 1

def getCapacity(caminho,demandm):
    capcam=0
    for x in caminho:
        capcam+=demandm[int(x)][1]
    return capcam

def getDistance(caminho,distm):
    distcam=0
    last=0
    for x in caminho:
        distcam+=distm[x][last]
        last=x
    return distcam

def construcaoGulosa(distm,demandm,cap,outroscaminhos):
    caminho=[0]
    exclusoes=[]
    while(isValid(caminho,demandm,cap)):
        pontoAtual=caminho[-1]
        minimo=0
        minIndex=0
        primeiro=1
        for index,linha in enumerate(distm):
            if((index in caminho) or (index in outroscaminhos)or (index in exclusoes)):
                continue
            elif(primeiro):
                    minimo=linha[pontoAtual]
                    minIndex=index
                    primeiro=0
                    continue
            elif(linha[pontoAtual]<minimo):
                    minimo=linha[pontoAtual]
                    minIndex=index
        if(minimo==0):
            break
        if(getCapacity(caminho,demandm)+demandm[minIndex][1]>cap):
            exclusoes.append(minIndex)
        else:
            caminho.append(minIndex)
    caminho.append(0)
    return caminho

dim,veic,cap,demandm,distm = getInfo("instancias_teste\P-n23-k8.txt")
caminhos=[0 for x in range(veic)]
outroscaminhos=[]
distanciatotal=0
for veiculo in range(0,veic):
    caminhos[veiculo]=construcaoGulosa(distm,demandm,cap,outroscaminhos)
    outroscaminhos+=caminhos[veiculo]
    distanciatotal+=getDistance(caminhos[veiculo],distm)
    print(caminhos[veiculo])
    print(getCapacity(caminhos[veiculo],demandm))
    print(getDistance(caminhos[veiculo],distm))
print(distanciatotal)
    
