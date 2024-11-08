# Modelo para guardar os registos de temperatura e precipitação ao longo de vários dias

# TabMeteo = [(Data,TempMin,TempMax,Precipitacao)]
    # Data = (Int,Int,Int)
    # TempMin = Float
    # TempMax = Float
    # Precipitacao = Float

import matplotlib.pyplot as plt

tabMeteo1 = [((2022,1,20), 2, 16, 0),((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]
t=[]

# Definição das funções
def menu():
    print("-------- Temperatura e precipitação ao longo de vários dias ----------")
    print("1) Temperatura média de cada dia")
    print("2) Guardar uma tabela meteorológica num ficheiro")
    print("3) Carregar uma tabela meteorológica de um ficheiro")
    print("4) Temperatura mínima")
    print("5) Amplitude térmica de cada dia")
    print("6) Dia e valor da precipitação máxima")
    print("7) Dias em que a precipitação foi superior a p")
    print("8) Maior número de dias consecutivos com precipitação abaixo de p")
    print("9) Gráficos de temperatura mínima, máxima e pluviosidade")
    print("0) Sair da aplicação")

def medias(tabMeteo):
    res = []
    for data,tmin,tmax,precip in tabMeteo:
        res.append((data, (tmin+tmax)/2))
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w")
    for data, tmin, tmax, precip in t:
        linha = f"{data[0]}::{data[1]}::{data[2]}::{tmin}::{tmax}::{precip}\n"
        f.write(linha)
    f.close()
    return len(t)

def carregaTabMeteo(fnome):
    res = []
    f = open(fnome, "r") 
    for linha in f:
            campos = linha.split('::') 
            data = (int(campos[0]),int(campos[1]),int(campos[2]))  
            res.append((data,float(campos[3]),float(campos[4]),float(campos[5])))  
    f.close()
    return res

def minMin(tabMeteo):
    minima = tabMeteo[0][1]
    for _,tmin,*_ in tabMeteo[1:]:
        if tmin < minima:
            minima = tmin
    return minima

def amplTerm(tabMeteo):
    res = []
    for data,tmin,tmax,precip in tabMeteo:
        res.append((data,tmax-tmin))
    return res 

def maxChuva(tabMeteo):
    max_prec = tabMeteo[0][3]   
    max_data=tabMeteo[0][0]
    for data,_,_,precip in tabMeteo[1:]:  
        if precip > max_prec:
            max_prec = precip
            max_data=data
    return (max_data, max_prec)

## ACABAR ?????
def diasChuvosos(tabMeteo, p):
    res=[]
    for data, tmin, tmax, precip in tabMeteo:
        if precip >p:
            res.append((data,precip))
    return res

def maxPeriodoChuva(tabMeteo, p): 
    consecutivos = 0
    contador =0
    for *_, precip in tabMeteo:
        if precip < p:
            contador = contador + 1
        else:
            contador = 0
    if consecutivos < contador:
            consecutivos = contador
    return consecutivos


def grafTabMeteo(t):
    datas = [f"{data[0]}/{data[1]}/{data[2]}" for data, _, _, _ in t]
    tmin = [registo[1] for registo in t]
    tmax = [registo[2] for registo in t]
    precip = [registo[3] for registo in t]

    plt.figure(figsize=(12,8))

    plt.subplot(3,1,1)
    plt.plot(datas, tmin, color='blue', marker='o', linestyle='-')
    plt.title('TEMPERATURA MÍNIMA')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (ºC)')
    plt.xticks(rotation=45)

    plt.subplot(3,1,2)
    plt.plot(datas, tmax, color='red', marker='o', linestyle='-')
    plt.title('TEMPERATURA MÁXIMA')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (ºC)')
    plt.xticks(rotation=45)

    plt.subplot(3,1,3)
    plt.bar(datas, precip, color='green')
    plt.title('PRECIPITAÇÃO')
    plt.xlabel('Data')
    plt.ylabel('Precipitação (mm)')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# Corpo da aplicação
menu()
op = input("Introduza a opção desejada:")
while op != '0':
    if op == '1':
        print(medias(tabMeteo1))
    elif op == '2':
        guardaTabMeteo(tabMeteo1, "meteorologia.txt")     
        print("Dados meteorológicos guardados em 'meteorologia.txt'")
    elif op == '3':
        print(carregaTabMeteo("meteorologia.txt"))
    elif op == '4':
        print(f"A temperatura mínima foi: {minMin(tabMeteo1)}")
    elif op == '5':
        print(amplTerm(tabMeteo1))
    elif op == '6':
        print(maxChuva(tabMeteo1))
    elif op == '7':
        p=float(input("Indique o valor p:"))
        print(diasChuvosos(tabMeteo1, p))
    elif op == '8':
        p=float(input("Indique o valor p:"))
        print(maxPeriodoChuva(tabMeteo1, p))
    elif op == '9':
        grafTabMeteo(tabMeteo1)
    else:
        print("Opção inválida. Por favor introduza uma das opções do menu")
    
    menu()
    op = input("Introduza a opção desejada:")
print("Obrigado, volte sempre!")