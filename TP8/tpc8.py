    # TPC_1
#a)
lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]  
ncomuns = []
for elemento in lista1:
    if elemento not in lista2:
        ncomuns.append(elemento)

for elemento in lista2:
    if elemento not in lista1:
        ncomuns.append(elemento)
print(ncomuns)

#b)
texto = """Vivia há já não poucos anos algures num concelho do Ribatejo 
    um pequeno lavrador e negociante de gado chamado Manuel Peres Vigário"""
lista =[]
for palavra in texto.split():
    if len(palavra)>3:
        lista.append(palavra)
print(lista)

#c)
lista = ['anaconda', 'burro', 'cavalo', 'macaco']
listaRes = []
i=1
for palavra in lista:
    listaRes.append((i,palavra))
    i=i+1
print(listaRes)

    #TPC2

#a)
def strCount(s, subs):
    contador = 0
    i = 0
    while i < len(s):
        if s[i:i+len(subs)] == subs:
            contador = contador + 1
            i = i + len(subs)
        else:
            i = i + 1
    return contador

print(strCount("catcowcat", "cat")) # --> 2
print(strCount("catcowcat", "cow")) # --> 1
print(strCount("catcowcat", "dog")) # --> 0

#b)
# Utilizando o sort
def produtoM3(lista):
    lista.sort()
    return lista[0] * lista[1] * lista[2]

# Sem utilizar o sort
def produtoM3_(lista):
    for i in range(len(lista)):
        for a in range(0, len(lista) - i - 1):
            if lista[a] > lista[a+1]:
                lista[a], lista[a+1]=lista[a+1], lista[a]
    return lista[0] * lista[1] * lista[2]

print(produtoM3([12,3,7,10,12,8,9]))
print(produtoM3_([12,3,7,10,12,8,9]))

#c)
def reduxInt(n):
    while n >= 10:
        total = 0
        for digito in str(n):
            total = total+ int(digito)
            n= total
    return n

print(reduxInt(38))
print(reduxInt(777))
print(reduxInt(3))

#d)
def myIndexOf(s1, s2):
    for i in range(len(s1) - len(s2) + 1):
        if s1[i:i+len(s2)] == s2:
            return i
    return -1

print(myIndexOf("Hoje está um belo dia de sol!", "belo"))
print(myIndexOf("Hoje está um belo dia de sol!", "chuva"))

    #TPC3 - Rede Social

#Considere o seguinte exemplo:
MyFaceBook = [
    {'id': 'p1', 'conteudo': 'A tarefa de avaliação é talvez a mais ingrata das tarefas que um professor tem de realizar...', 'autor': 'jcr', 
    'dataCriacao': '2023-07-20', 'comentarios': [{'comentario': 'Completamente de acordo...','autor': 'prh'},{'comentario': 'Mas há quem goste...','autor': 'jj'}]},
    {'id': 'p2', 'conteudo': 'Segundo post', 'autor': 'a', 'dataCriacao': '2023-12-2', 'comentarios':[{'comentario':'abc', 'autor':'a'}]}
]

#a)
def quantosPost(redeSocial):
    return len(redeSocial)

print(quantosPost(MyFaceBook))

#b)
def postsAutor(redeSocial, autor):
    for post in redeSocial:
        if post['autor'] == autor:
            return post

print(postsAutor(MyFaceBook, 'jcr'))
print(postsAutor(MyFaceBook, 'a'))

#c)
def autores(redeSocial):
    lista_autores=[]
    for post in redeSocial:
        if 'autor' in post:
            lista_autores.append(post['autor'])
    return sorted(lista_autores)

print(autores(MyFaceBook))

#d)
def insPost(redeSocial, conteudo, autor, dataCriacao, comentarios):
    ids = [int(post['id'][1:]) for post in redeSocial if 'id' in post]
    novo_id = f"p{max(ids) + 1}" if ids else "p1"
    novo_post = {
        'id': novo_id,
        'conteudo': conteudo,
        'autor': autor,
        'dataCriacao': dataCriacao,
        'comentarios': comentarios
    }
    redeSocial.append(novo_post)
    return redeSocial

novo_conteudo = 'Terceito post'
novo_autor = 'b'
nova_data = '2023-04-26'
novos_comentarios = []

MyFaceBook= insPost(MyFaceBook, novo_conteudo, novo_autor, nova_data, novos_comentarios)

print("Lista de posts após adicionar o novo post:")
for post in MyFaceBook:
    print(post)

#e)
def remPost(redeSocial, id):
    nova_rede = []
    for post in redeSocial:
        if post['id'] != id:
            nova_rede.append(post)
    redeSocial[:] = nova_rede
    print(f"Id '{'p1'}' removido com sucesso")
removido = remPost(MyFaceBook, 'p1')
print("MyFaceBook após a remoção:", MyFaceBook)

#f)
def postsPorAutor(redeSocial):
    distribuiçao = {}
    for post in redeSocial:
        autor = post['autor']
        if autor in distribuiçao:
            distribuiçao[autor] = distribuiçao[autor] + 1
        else:
            distribuiçao[autor] = 1
    return distribuiçao

distribuiçao = postsPorAutor(MyFaceBook)
print("Distribuição de posts por autor:", distribuiçao)

#g)
def comentadoPor(redeSocial, autor):
    posts_comentados = []
    for post in redeSocial:
        for comentario in post['comentarios']:
            if 'autor' in comentario and comentario['autor'] == autor:
                posts_comentados.append(post)
    return posts_comentados

resultado = comentadoPor(MyFaceBook, 'a')
for post in resultado:
    print(post)
