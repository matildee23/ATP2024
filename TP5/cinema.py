## Gestão de salas de cinema de um centro comercial

## cinema = [sala]
## sala = (nlugares, vendidos, filme)
## nlugares = Int
## filme = string 
## vendidos = [Int]

## definição das funções
def menu():
    cinema = []
    print("------ Gestão do cinema ------")
    print("1) Listar filmes em exibição")
    print("2) Listar disponibilidades")
    print("3) Verificar disponibilidade de um lugar")
    print("4) Vender bilhete")
    print("5) Inserir nova sala")
    print("6) Encontrar uma sala")
    print("0) Sair")



def listar(cinema1):
    print("Filmes em exibição:")
    for sala in cinema1:
        print(f"{sala[2]}")

def disponivel(cinema1, filme, lugar):
    for sala in cinema1:
        if sala[2] == filme:
            return lugar not in sala[1]
    return False

def vendebilhete(cinema1, filme, lugar):
    novo_cinema = []
    for sala in cinema1:
        if sala[2] == filme:
            if lugar not in sala[1] and lugar < sala [0]:
                nova_sala = (sala[0], sala[1] + [lugar], sala[2])
                novo_cinema.append(nova_sala)
            else:
                novo_cinema.append(sala)
        else:
            novo_cinema.append(sala)
    return novo_cinema

def listardisponibilidades(cinema1):
    print("Disponibilidade das salas:")
    for i,sala in enumerate(cinema1):
        lugares_disponiveis = sala [0] - len(sala[1])
        print(f"Sala {i+1} - Filme: '{sala[2]}' e há {lugares_disponiveis} lugares disponíveis")

def inserirsala(cinema1, nova_sala):
    for sala in cinema1:
        if sala == nova_sala:
            print("Essa sala já existe.")
            return cinema1
    print(f"A sala com o filme '{nova_sala[2]}' foi inserida com sucesso no cinema!")
    return cinema1 + [nova_sala]


## Outra função que pode ser útil
def encontrarsala(cinema1):
    filme = input("Introduza o nome do filme que deseja procurar:")
    for i, sala in enumerate(cinema1):
        if sala[2] == filme:
            print(f"O filme '{filme}' encontra-se em exibição na sala {i+1}")
            return i+1, sala
    print(f"O filme {filme} não foi encontrado")
    return None, None


sala1 = (150, [], "Twilight")
sala2 = (200, [], "Hannibal")
cinema1 = []

cinema1 = inserirsala(cinema1,sala1)
cinema1 = inserirsala(cinema1,sala2)



## Corpo da aplicação
menu()
op = input("Introduza uma das seguintes opções:")
while op != "0":
    if op == "1":
        listar(cinema1)
    
    elif op == "2":
        listardisponibilidades(cinema1)
    
    elif op == "3":
        filme = input("Introduza o filme que deseja ver:")
        lugar = int(input("Introduza o lugar que pretende:"))
        if disponivel(cinema1, filme, lugar):
            print(f"O lugar {lugar} para o filme '{filme}' está disponível")
        else:
            print(f"O lugar {lugar} para o filme '{filme}' está ocupado ou não existe")
    
    elif op == "4":
        filme = input("Introduza o filme que deseja ver:")
        lugar = int(input("Introduza o lugar que pretende:"))
        if disponivel(cinema1, filme, lugar):
            cinema1 = vendebilhete(cinema1, filme, lugar)
            print(f"O bilhete no lugar {lugar} para o filme '{filme}' foi vendido com sucesso!")
        else:
            print(f"O lugar {lugar} para o filme '{filme}' não está disponível")

    elif op == "5":
        nlugares = int(input("Introduza o número total de lugares na sala:"))
        filme = input("Introduza o filme em exibição na sala:")
        sala = (nlugares, [], filme)
        cinema1 = inserirsala(cinema1, sala)

    elif op == "6":
        encontrarsala(cinema1)
    
    else:
        print("Opção inválida. Por favor introduza uma das opções do menu.")

    menu()
    op = input("Introduza uma das seguintes opções:")   
print("Obrigado, volte sempre!")