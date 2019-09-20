import copy
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

def isValid(caminho,demandm,cap): #pega a rota, soma a capacidade dela junto com sua demanda disponível
    capcam=0
    for x in caminho:
        capcam+=demandm[int(x)][1]
    if(capcam>cap):
        return 0
    else:
        return 1 #não é válido se não melhora a distância ou não tem capacidade
    
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

def trocaVizinhanca(caminhos,distm,demandm,cap,iteracoes):
    teste=0
    for index1,caminho1 in enumerate(caminhos):
        for index2,caminho2 in enumerate(caminhos):
            if(index2<=index1):
                continue
            caminho1temp=copy.deepcopy(caminho1)
            caminho2temp=copy.deepcopy(caminho2)
            caminho1min=copy.deepcopy(caminho1)
            caminho2min=copy.deepcopy(caminho2)
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
                caminho1[caminho1.index(minIndex[0])]=minIndex[1]
                caminho2[caminho2.index(minIndex[1])]=minIndex[0]
                if(isValid(caminho1,demandm,cap) and isValid(caminho2,demandm,cap)):
                    caminhototal=getDistance(caminho1,distm)+getDistance(caminho2,distm)
                    caminhototalmin=getDistance(caminho1min,distm)+getDistance(caminho2min,distm)
                    if(caminhototal<caminhototalmin):
                        caminho1min=copy.deepcopy(caminho1)
                        caminho2min=copy.deepcopy(caminho2)
                    exclusoes.append(minIndex)
                else:
                    exclusoes.append(minIndex)
                    caminho1[caminho1.index(minIndex[1])]=int(minIndex[0])
                    caminho2[caminho2.index(minIndex[0])]=int(minIndex[1])
                    continue
            if(getDistance(caminho1min,distm)+getDistance(caminho2min,distm)< getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm)
                   and isValid(caminho1min,demandm,cap) and isValid(caminho2min,demandm,cap)):
                print("DISTANCIAS",getDistance(caminho1min,distm)+getDistance(caminho2min,distm),getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm))
                caminhos[index1]=copy.deepcopy(caminho1min)
                caminhos[index2]=copy.deepcopy(caminho2min)
                #print(caminhos)
                return caminhos

    return caminhos



#=========================================================================================================================================================================================
def roubaVizinhanca(caminhos,distm,demandm,cap,iteracoes):
    teste=0
    for index1,caminho1 in enumerate(caminhos):
        for index2,caminho2 in enumerate(caminhos):
            #print(caminhos)
            if(index2<=index1):
                continue
            caminho1temp=copy.deepcopy(caminho1)
            caminho2temp=copy.deepcopy(caminho2)
            caminho1min=copy.deepcopy(caminho1)
            caminho2min=copy.deepcopy(caminho2)
            exclusoes=[]
            caminhototalmin=0
            for i in range(0,iteracoes):
                caminho1=copy.deepcopy(caminho1min)
                caminho2=copy.deepcopy(caminho2min)
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
                inseriu=0
                for i in [0,1]:
                    caminho1.insert(caminho1.index(minIndex[0])+i,minIndex[1])
                    if(i==0):
                        caminho2.remove(minIndex[1])
                    if(isValid(caminho1,demandm,cap)):
                        caminhototal=getDistance(caminho1,distm)
                        caminhototalmin=getDistance(caminho1min,distm)
                        if(caminhototal<caminhototalmin):
                            caminho1min=copy.deepcopy(caminho1)
                            caminho2min=copy.deepcopy(caminho2)
                        else:
                            caminho1=copy.deepcopy(caminho1min)
                            caminho2=copy.deepcopy(caminho2min)
                        exclusoes.append(minIndex)
                        inseriu=1
                        break
                    else:
                        if(i==1):
                            exclusoes.append(minIndex)
                        caminho1.remove(minIndex[1])
                        continue
                if(not inseriu):
                    caminho1=copy.deepcopy(caminho1min)
                    caminho2=copy.deepcopy(caminho2min)
                    exclusoes.remove(minIndex)
                    for j in [0,1]:
                        caminho2.insert(caminho2.index(minIndex[1])+j,minIndex[0])
                        if(j==0):
                            caminho1.remove(minIndex[0])
                        if(isValid(caminho2,demandm,cap)):
                            caminhototal=getDistance(caminho2,distm)
                            caminhototalmin=getDistance(caminho2min,distm)
                            if(caminhototal<caminhototalmin):
                                caminho1min=copy.deepcopy(caminho1)
                                caminho2min=copy.deepcopy(caminho2)
                            else:
                                caminho1=copy.deepcopy(caminho1min)
                                caminho2=copy.deepcopy(caminho2min)
                            exclusoes.append(minIndex)
                            inseriu=1
                            break
                        else:
                            if(j==1):
                                exclusoes.append(minIndex)
                            caminho2.remove(minIndex[0])
                            continue
                if(getDistance(caminho1min,distm)+getDistance(caminho2min,distm)< getDistance(caminho1temp,distm)+getDistance(caminho2temp,distm)
                    and (isValid(caminho1min,demandm,cap) and isValid(caminho2min,demandm,cap))):
                    #print(caminhos)
                    caminhos[index1]=copy.deepcopy(caminho1min)
                    caminhos[index2]=copy.deepcopy(caminho2min)
                    #print(caminhos)
                    return caminhos
    return caminhos
#=======================================================================================================================================================
def organizaVizinhanca(caminhos,distm,demandm,cap,iteracoes):
    teste=0
    for index1,caminho1 in enumerate(caminhos):
        caminho1temp=copy.deepcopy(caminho1)
        caminho1min=copy.deepcopy(caminho1)
        exclusoes=[]
        caminhototalmin=0
        for i in range(0,iteracoes):
            caminho1=copy.deepcopy(caminho1min)
            minimo=0
            minIndex=[0,0]
            minFlag=1
            for ponto1 in caminho1:
                if(ponto1==0):
                        continue
                for ponto2 in caminho1:
                    if(ponto2==0 or ponto1==ponto2):
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
                caminho1[caminho1.index(minIndex[0])]=minIndex[1]
                caminho1[caminho1.index(minIndex[1])]=minIndex[0]
                if(isValid(caminho1,demandm,cap)):
                    caminhototal=getDistance(caminho1,distm)
                    caminhototalmin=getDistance(caminho1min,distm)
                    if(caminhototal<caminhototalmin):
                        caminho1min=copy.deepcopy(caminho1)
                    exclusoes.append(minIndex)
                else:
                    exclusoes.append(minIndex)
                    caminho1[caminho1.index(minIndex[1])]=int(minIndex[0])
                    caminho2[caminho2.index(minIndex[0])]=int(minIndex[1])
                    continue
            if(getDistance(caminho1min,distm)< getDistance(caminho1temp,distm)
                   and isValid(caminho1min,demandm,cap)):
                #print(caminhos)
                caminhos[index1]=copy.deepcopy(caminho1min)
                #print(caminhos)
                return caminhos

    return caminhos

#===================================================================================
def VND(caminhos,distm,demandm,cap,iteracoes):
    todoscaminhos=copy.deepcopy(caminhos)
    for k in range(0,3):
        print(k)
        print("Antes:",getArrayDistance(todoscaminhos,distm))
        if(k==0):
            todoscaminhos=trocaVizinhanca(copy.deepcopy(todoscaminhos),distm,demandm,cap,iteracoes)
        elif(k==1):
            todoscaminhos=roubaVizinhanca(copy.deepcopy(todoscaminhos),distm,demandm,cap,iteracoes)
        elif(k==2):
            todoscaminhos=organizaVizinhanca(copy.deepcopy(todoscaminhos),distm,demandm,cap,iteracoes)
        print("Depois:",getArrayDistance(todoscaminhos,distm))
    return todoscaminhos



#==============================================================================
import os
currentfolder=os.getcwd()
dim,veic,cap,demandm,distm = getInfo(currentfolder+"/instancias_teste/P-n55-k7.txt")
caminhos=[0 for x in range(veic)]
outroscaminhos=[]
todoscaminhos=[]
distanciatotal=0
for veiculo in range(0,veic): #interação para verificar a qtd de veículos disponíveis
    caminhos[veiculo]=construcaoGulosa(distm,demandm,cap,outroscaminhos)
    outroscaminhos+=caminhos[veiculo]
    distanciatotal+=getDistance(caminhos[veiculo],distm)
    todoscaminhos.append(caminhos[veiculo])
if(allPointsVisited(todoscaminhos,dim)):
    print("Todos os pontos foram visitados")
else:
    print("Pontos deixados de fora")
for x in range(0,50):
    #print("Antes:",getArrayDistance(todoscaminhos,distm))
    todoscaminhos=VND(copy.deepcopy(todoscaminhos),distm,demandm,cap,1000)
    #print("Depois:",getArrayDistance(todoscaminhos,distm))
    if(allPointsVisited(todoscaminhos,dim)):
        print("Todos os pontos foram visitados")
    else:
        print("Pontos deixados de fora")
