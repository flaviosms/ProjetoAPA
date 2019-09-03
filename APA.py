
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

def movimentoVizinhanca(caminhos,distm,demandm,cap,iteracoes):
    for index1,caminho1 in enumerate(caminhos):
        for caminho2 in caminhos[index1+1:]:
            caminho1temp=caminho1
            caminho2temp=caminho2
            exclusoes=[]
            for i in range(0,iteracoes):
                minimo=0
                minIndex=[0,0]
                minFlag=1
                for ponto1 in caminho1:
                    if(ponto1==0):
                            continue
                    for ponto2 in caminho2:
                        if(ponto2==0):
                            continue
                        if(minFlag and not [ponto1,ponto2] in exclusoes):
                            minimo=distm[ponto1][ponto2]
                            minIndex=[ponto1,ponto2]
                            minFlag=0
                        elif(distm[ponto1][ponto2]<minimo and not [ponto1,ponto2] in exclusoes):
                            minimo=distm[ponto1][ponto2]
                            minIndex=[ponto1,ponto2]
                if(minFlag):
                    continue
                DistanciaTotal=getDistance(caminho1,distm)+getDistance(caminho2,distm)
                caminho1[caminho1.index(minIndex[0])]=minIndex[1]
                caminho2[caminho2.index(minIndex[1])]=minIndex[0]
                print(str(isValid(caminho1,demandm,cap)) + "\t"+ str(isValid(caminho2,demandm,cap))+ "\t"+ str(getDistance(caminho1,distm)+getDistance(caminho2,distm)) + "\t"+ str(DistanciaTotal))
                if(isValid(caminho1,demandm,cap) and isValid(caminho2,demandm,cap)):
                    print("Trocou")
                    print([ponto1,ponto2])
                    exclusoes.append(minIndex)
                else:
                    exclusoes.append(minIndex)
                    caminho1[caminho1.index(minIndex[1])]=minIndex[0]
                    caminho2[caminho2.index(minIndex[0])]=minIndex[1]
            if(getDistance(caminho1,distm)+getDistance(caminho2,distm)>= getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm)):
                caminho1=caminho1temp
                caminho2=caminho2temp
                print("Sem ganho")
                #print(minimo)
                #print(minIndex)
                #print(caminho1)
                #print(caminho2)
                                


dim,veic,cap,demandm,distm = getInfo("instancias_teste\P-n20-k2.txt")
caminhos=[0 for x in range(veic)]
outroscaminhos=[]
todoscaminhos=[]
distanciatotal=0
for veiculo in range(0,veic):
    caminhos[veiculo]=construcaoGulosa(distm,demandm,cap,outroscaminhos)
    outroscaminhos+=caminhos[veiculo]
    distanciatotal+=getDistance(caminhos[veiculo],distm)
    todoscaminhos.append(caminhos[veiculo])
    #print(caminhos[veiculo])
    #print(getCapacity(caminhos[veiculo],demandm))
    #print(getDistance(caminhos[veiculo],distm))
#print(distanciatotal)
movimentoVizinhanca(todoscaminhos,distm,demandm,cap,99)
    
