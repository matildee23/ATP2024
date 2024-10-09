import random
def menu():
    print("MENU")
    print("1) Criar lista")
    print("2) Ler lista")
    print("3) Soma")
    print("4) Média")
    print("5) Maior")
    print("6) Menor")
    print("7) A lista está ordenada por ordem crescente?")
    print("8) A lista está ordenada por ordem decrescente?")    
    print("9) Procura um elemento")
    print("0) Sair")


def criar_lista(tamanho):
    lista = [random.randint(1,100) for _ in range(tamanho)]
    return lista

def lista_user(tamanho):
    lista=[]
    for i in range(tamanho):
        numero=int(input(f"Introduza o número {i+1}/{tamanho}:"))
        lista.append(numero)
    return lista

def soma(lista):
    res=0
    for x in lista:
        res=res+x
    return res

def mediaLista(lista):
    res=0
    i=0
    while i<len(lista):
        res=res+lista[i]
        i=i+1
    media=res/len(lista)
    return media

def maiorLista(lista):
    res=lista[0]
    for x in lista:
        if x>res:
            res=x
    return res


def menorLista(lista):
    res=lista[0]
    for x in lista:
        if x<res:
            res=x
    return res

def estaCrescente(lista):
    res=True
    i=0
    while res and i<len(lista)-1:
        if lista[i] > lista[i+1]:
            res=False
        else:
            i=i+1
    return res

def estaDecrescente(lista):
    res=True
    i=0
    while res and i<len(lista)-1:
        if lista[i] < lista[i+1]:
            res=False
        else:
            i=i+1
    return res

def procuraElemento(lista):
    num = int(input("Introduza o número do elemento que deseja procurar na lista:"))
    i=0
    for i in range(len(lista)):
        if lista[i] == num:
            return i
    return -1




## Programa principal
import random
menu()
opcao = input("Selecione a opção desejada:")
while opcao != "0":
    if opcao == "1":
        tamanho=int(input("Introduza o tamanho da lista:")) 
        lista = criar_lista(tamanho)
        print("A lista aleatória criada é:", lista)
    
    elif opcao == "2":
        tamanho=int(input("Introduza o tamanho da lista:"))
        lista=lista_user(tamanho)
        print("A lista obtida pelo utilizador é:", lista)

    elif opcao == "3":
        print(f"A soma da lista é: {soma(lista)}")
    
    elif opcao == "4":
        print(f"A média da lista é: {mediaLista(lista)}")

    elif opcao == "5":
        print(f"O maior elemento da lista é: {maiorLista(lista)}")

    elif opcao == "6":
        print(f"O menor elemento da lista é: {menorLista(lista)}")

    elif opcao == "7":
        if estaCrescente(lista) == True:
            print("Sim") #### nao esta a dar
        else:
            print("Não")
        
    elif opcao == "8":
        if estaDecrescente(lista) == True:
            print("Sim")
        else:
            print("Não")

    elif opcao == "9":
        print(procuraElemento(lista))

    menu()
    opcao = input("Selecione a opção desejada:")
print("Obrigado, volte sempre!")