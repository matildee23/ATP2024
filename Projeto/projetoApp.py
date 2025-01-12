import projeto

def menu():
    menu = """
--------- Menu de Consulta e Análise de Publicações Científicas ---------

(1) Carregar o dataset
(2) Guardar o dataset
(3) Inserir um novo registo
(4) Apagar um registo
(5) Consultar um registo
(6) Listar os registos
(7) Listar autores
(8) Gráficos de várias distribuições
(9) Exportar dados para um ficheiro
(10) Help
(0) Sair
"""
    print(menu)

mybd = []
dataset_carregado = False
resultados = []

# App principal
menu()
op = input("Introduza uma opção:")
while op != "0":
    if op == "1":
        if not dataset_carregado:
            mybd = projeto.carregarBD("ata_medica_papers.json")
            print("O ficheiro foi carregado com sucesso!")
            dataset_carregado = True
        else:
            print("O ficheiro já foi carregado anteriormente.")
    elif op == "2":
        projeto.guardarBD(mybd, "ata_medica_papers.json")
    elif op == "3":
        mybd = projeto.inserir_registo(mybd)
        if mybd:
            print(mybd)
    elif op == "4":
        doi = input("Introduza o DOI associado ao registo que deseja apagar:")
        mybd = projeto.apagar(mybd, doi)
        if mybd:
            print(mybd)
    elif op == "5":
        doi = input("Introduza o DOI identificador da publicação:")
        resultados = projeto.consultarD(mybd, doi)
        if resultados:
            print("Registo encontrado:")
            print(resultados)
        else:
            print("Não foi encontrado nenhum registo com o DOI fornecido.")
    elif op == "6":
        resultados = projeto.listar_publicacoes(mybd)
        if resultados:
            print(resultados)
        else:
            print("Nenhuma publicação encontrada com o critério fornecido.")
    elif op == "7":
        resultados = projeto.listar_autores(mybd)  
        if resultados:
            print(resultados)            
    elif op == "8":
        gráficos = projeto.distrib(mybd)
        if gráficos:
            print("Gráfico criado com sucesso!")
    elif op == "9":
        fnome = input("Introduza um nome para o ficheiro (nome.json) para qual pretende exportar os dados:")
        if resultados:
            projeto.exportar_dados(fnome, resultados)
            print("Dados exportados com sucesso!")
        else:
            print("Não há dados para exportar.")
    elif op == "10":
        projeto.help()

    menu()
    op= input("Introduza uma opção:")

print("Obrigado, volte sempre!")