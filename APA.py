
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
def allPointsVisited(caminhos,dim):
    pontos=[x for x in range(0,dim-1)]
    for caminho in caminhos:
        for letra in caminho:
            if(int(letra) in pontos):
                pontos.pop(pontos.index(int(letra)))
                continue
    if(pontos==[]):
       return 1 
    return 0

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
def getArrayDistance(caminhos,distm):
    result=0
    for caminho in caminhos:
        result+=getDistance(caminho,distm)
    return result

def construcaoGulosa(distm,demandm,cap,outroscaminhos):
    caminho=[0]
    exclusoes=[]
    while(isValid(caminho,demandm,cap)):
        pontoAtual=caminho[-1]
        maximo=0
        maxIndex=0
        primeiro=1
        for index,linha in enumerate(demandm):
            if((index in caminho) or (index in outroscaminhos)or (index in exclusoes)):
                continue
            elif(getCapacity(caminho,demandm)+linha[1]>cap):
                exclusoes.append(maxIndex)
                continue
            elif(primeiro):
                    maximo=linha[1]
                    maxIndex=index
                    primeiro=0
                    continue
            elif(linha[1]>maximo):
                    maximo=linha[1]
                    maxIndex=index
        if(maximo==0):
            break
        if(getCapacity(caminho,demandm)+demandm[maxIndex][1]>cap):
            exclusoes.append(maxIndex)
        else:
            caminho.append(maxIndex)
    caminho.append(0)
    return caminho

def movimentoVizinhanca(caminhos,distm,demandm,cap,iteracoes):
    teste=0
    caminhos2=[x for x in caminhos]
    for index1,caminho1 in enumerate(caminhos):
        for index2,caminho2 in enumerate(caminhos2):
            if(index2<index1):
                continue
            #print("index:",index1,index2,sep='\t')
            caminho1temp=[x for x in caminho1]
            caminho2temp=[x for x in caminho2]
            caminho1min=[x for x in caminho1]
            caminho2min=[x for x in caminho2]
            exclusoes=[]
            caminhototalmin=0
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
                
                
                #print(str(isValid(caminho1,demandm,cap)) + "\t"+ str(isValid(caminho2,demandm,cap))+ "\t"+ str(getDistance(caminho1,distm)+getDistance(caminho2,distm)) + "\t"+ str(DistanciaTotal))
                if(isValid(caminho1,demandm,cap) and isValid(caminho2,demandm,cap)):
                    caminhototal=getDistance(caminho1,distm)+getDistance(caminho2,distm)
                    caminhototalmin=getDistance(caminho1min,distm)+getDistance(caminho2min,distm)
                    #print(caminhototal,caminhototalmin,sep='\t ')
                    #print(caminhototal,caminhototalmin,sep='\t')
                    if(caminhototal<caminhototalmin):
                        caminho1min=[x for x in caminho1]
                        caminho2min=[x for x in caminho2]
                    exclusoes.append(minIndex)
                else:
                    exclusoes.append(minIndex)
                    caminho1[caminho1.index(minIndex[1])]=int(minIndex[0])
                    caminho2[caminho2.index(minIndex[0])]=int(minIndex[1])
            #print(getDistance(caminho1min,distm)+getDistance(caminho2min,distm),getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm),sep='\t')
            if(getDistance(caminho1min,distm)+getDistance(caminho2min,distm)>= getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm)):
                caminhos[index1]=[x for x in caminho1temp]
                caminhos[index2+1]=[x for x in caminho2temp]
                #print("Sem ganho")
            else:
                
                print("Caminho antes troca:",caminhos[index1],caminhos[index2],getArrayDistance([caminhos[index1],caminhos[index2]],distm),sep='\t')
                print("Caminho minimo ptro:",caminho1min,caminho2min,getArrayDistance([caminho1min,caminho2min],distm),sep='\t')
                caminhos[index1]=[x for x in caminho1min]
                caminhos[index2]=[x for x in caminho2min]
                print("Caminho depois troca:",caminhos[index1],caminhos[index2],getArrayDistance([caminhos[index1],caminhos[index2]],distm),sep='\t')
                print("\n")
                #print("Ganho encontrado")
                #print(minimo)
                #print(minIndex)
                #print(caminho1)
                #print(caminho2)
                                


dim,veic,cap,demandm,distm = getInfo("instancias_teste\P-n45-k5.txt")
caminhos=[0 for x in range(veic)]
outroscaminhos=[]
todoscaminhos=[]
distanciatotal=0
for veiculo in range(0,veic):
    caminhos[veiculo]=construcaoGulosa(distm,demandm,cap,outroscaminhos)
    outroscaminhos+=caminhos[veiculo]
    distanciatotal+=getDistance(caminhos[veiculo],distm)
    todoscaminhos.append(caminhos[veiculo])
    print(caminhos[veiculo])
    print(getCapacity(caminhos[veiculo],demandm))
    print(getDistance(caminhos[veiculo],distm))
#print("todoscaminhos:",len(todoscaminhos),sep='\t')
if(allPointsVisited(todoscaminhos,dim)):
    print("Todos os pontos foram visitados")
else:
    print("Pontos deixados de fora")
#print(distanciatotal)
#print(todoscaminhos)
for x in range(0,1):
    print("Antes:",getArrayDistance(todoscaminhos,distm))
    movimentoVizinhanca(todoscaminhos,distm,demandm,cap,1000)
    print("Depois:",getArrayDistance(todoscaminhos,distm))
