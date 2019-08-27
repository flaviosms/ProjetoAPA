f = open("instancias_teste/P-n16-k8.txt",'r')
edges=0
icounter=0
jcounter=0
for linha in f:
    if(not edges):
        if("NAME" in linha):
            name=str(linha.split()[-1:][0])
            print(name)
        if("DIMENSION" in linha):
            dim=int(linha.split()[-1:][0])
            print(dim)
            distm=[[0 for x in range(dim)] for y in range(dim)]
        if("VEHICLES" in linha):
            veic=int(linha.split()[-1:][0])
            print(veic)
        if("CAPACITY" in linha):
            cap=int(linha.split()[-1:][0])
            print(cap)
        if("EDGE_WEIGHT_SECTION" in linha):
            edges=True
    else:
        jcounter=0
        for v in linha.split():
            distm[icounter][jcounter]=v
            jcounter+=1
        icounter+=1
for x in distm:
    print(x)
    
