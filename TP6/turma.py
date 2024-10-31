# Aplicação para gestão de alunos

## Estrutura do aluno = (nome, id, [notaTPC, notaProj, notaTeste])
## Estrutura da turma = [aluno]


# definição das funções
def menu():
    turma = []
    print("----------- Gestão da turma -----------")
    print("1) Criar uma turma")
    print("2) Inserir um aluno na turma")
    print("3) Listar a turma")
    print("4) Consultar um aluno por id")
    print("5) Guardar a turma em ficheiro")
    print("6) Carregar uma turma dum ficheiro")
    print("0) Sair da aplicação")

turma = []

def criar():
    turma = []
    return turma

def obter_nota(qualquer_nota):
    nota = float(input(f"Introduza a {qualquer_nota} (0-20):"))
    while nota < 0 or nota > 20:
        print(f"A {qualquer_nota} deve estar entre 0 e 20.")
        nota = float(input(f"Introduza a {qualquer_nota} (0-20):"))
    return nota



def inserir_aluno(turma):
    nome = input("Introduza o nome do aluno:")
    id = int(input("Introduza o ID do aluno:"))
    for aluno in turma:
        if aluno[1] == id:
            print("Esse ID já existe")
            return None
    notaTPC = obter_nota("nota do TPC")
    notaProj = obter_nota("nota do projeto")
    notaTeste = obter_nota("nota do teste")
    aluno = (nome, id, [notaTPC, notaProj, notaTeste])
    turma.append(aluno)
    print("Aluno inserido na turma com sucesso!")


def listar(turma):
    if turma == []:
        print("Turma vazia")
    else:
        print("\n-----Lista de Alunos-----")
        for aluno in turma:
            print(f"Nome: {aluno[0]}\n ID: {aluno[1]}\n Nota TPC: {aluno[2][0]}\n Nota do Projeto: {aluno[2][1]}\n Nota do Teste: {aluno[2][2]}")
    
def consultar_aluno(turma, ID):
    for aluno in turma:
        if aluno [1]== ID:
            print(f"Nome: {aluno[0]}\n Nota do TPC: {aluno[2][0]}\n Nota do Projeto: {aluno[2][1]}\n Nota do Teste: {aluno[2][2]}")
        else:
            print("Aluno não encontrado!")

def guardar_turma(turma, fnome):
    file = open(fnome,"w")
    for aluno in turma:
        file.write(f"{aluno[0]}; {aluno[1]}; {aluno[2][0]}; {aluno[2][1]}; {aluno[2][2]}\n")
    file.close()
    print(f"Turma guardada com sucesso no ficheiro {fnome}!")

def carregar(fnome):
    turma=[]
    file = open(fnome, "r")
    for linha in file:
        partes = linha.split('; ')
        nome = partes[0]
        ID = partes[1]
        notas = [float(partes[2]), float(partes[3]), float(partes[4])]
        aluno = (nome, ID, notas)
        turma.append(aluno)
    file.close()
    return turma




## corpo da aplicação
menu()
op = input("Introduza a opção desejada:")

while op !='0':
    if op == '1':
        turma = criar()
        print("Nova turma criada com sucesso!")
    elif op == '2':
        inserir_aluno(turma)
    elif op == '3':
        listar(turma)
    elif op == '4':
        ID = int(input("Introduza o ID do aluno:"))
        consultar_aluno(turma, ID)
    elif op == '5':
        guardar_turma(turma, "turma.txt")
    elif op == '6':
        turma = carregar("turma.txt")
        print(turma)
    else:
        print("Opção inválida. Por favor introduza uma das opções do menu")
    
    menu()
    op = input("Introduza a opção desejada:")
print("Obrigado, volte sempre!")