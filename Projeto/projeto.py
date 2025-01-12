import json
import matplotlib.pyplot as plt


# Carregar a informação do dataset para uma estrutura de dados em memória
def carregarBD(fnome):
    f = open(fnome, encoding='utf-8')
    mybd = json.load(f)
    f.close()
    return mybd

# Guardar a estrutura de dados em memória num ficheiro
def guardarBD(mybd, fnome):
    fout = open(fnome, "w", encoding='utf-8')
    json.dump(mybd, fout, indent=4, ensure_ascii=False)
    fout.close()
    print(f"Dados salvos em {fnome} com sucesso!")

# Inserir um novo registo
def inserir_registo(mybd):
    print("Insira os dados para o novo registo:")
    title = input("  Título:")
    abstract = input("  Abstract:")
    keywords = input("  Palavras-chave (separadas por vírgula):")
    doi = input("  DOI:")
    publish_date = input("  Data de publicação (YYYY-MM-DD):")
    pdf = input("  PDF:")
    url = input("  URL:")

    authors_input = input("Insira os autores (nomes separados por vírgula):")
    affiliations_input = input("Insira as afiliações (separadas por vírgula): ")
    orcids_input = input("Caso pretenda, insira os ORCIDs dos autores (separados por vírgula):")

    authors = authors_input.split(",")
    affiliations = affiliations_input.split(",")
    orcids = orcids_input.split(",") if orcids_input else []

    if len(authors) < len(affiliations):
        print("Erro: O número de autores não corresponde ao número de afiliações.")
        return mybd

    author_list = []
    for i in range(len(authors)):
        author = {"name": authors[i], "affiliation": affiliations[i]}
        if i < len(orcids): 
            author["orcid"] = orcids[i]
        author_list.append(author)

    novo_registo = {
        "abstract": abstract,
        "keywords": keywords,
        "authors": author_list,
        "doi": doi,
        "pdf": pdf,
        "publish_date": publish_date,
        "title": title,
        "url": url
    }

    for registo in mybd:
        if registo["doi"] == novo_registo["doi"]:
            print("Erro. Esse registo já existe (mesmo DOI).")
            return mybd
    
    mybd.append(novo_registo)
    print("Novo registo adicionado com sucesso!")
    return mybd

# Apagar um registo
def apagar(mybd, doi):
    for i, reg in enumerate(mybd):
        if reg["doi"] == doi:
            del mybd[i]
            print(f"Registo com DOI '{doi}' foi apagado.")
            return mybd
    print(f"Registo com DOI '{doi}' não encontrado.")
    return mybd

# Consultar um registo com base no DOI - PARA O PONTO 5
def consultarD(mybd, doi):
    for reg in mybd:
        if reg["doi"] == doi:
            return reg
    print("Não foi encontrado nenhum registo com o DOI fornecido.")

# Listar as publicações presentes no sistema com base em vários critérios à escolha do user
def menu():
    menu = """
    Escolha um critério de pesquisa:
      1) Título
      2) Autor
      3) Afiliação
      4) Data de Publicação
      5) Palavras-chave
      0) Sair
      """
    
    print(menu)

def listar_publicacoes(mybd):
    resultados = []
    menu()
    escolha = input("Digite o número do critério que deseja usar: ")

    while escolha != '0':
        if escolha == '1':
            criterio = input("Introduza o título do artigo: ")
            for pub in mybd:
                if "title" in pub and pub["title"]:
                    if criterio.lower() == pub["title"].lower():
                        resultados.append(pub)
            return resultados
            
        elif escolha == '2':
            criterio = input("Introduza o nome do autor: ")
            for pub in mybd:
                for autor in pub["authors"]:
                    if criterio == autor["name"]:
                        resultados.append(pub)
            return resultados

        elif escolha == '3':
            criterio = input("Introduza a afiliação: ")
            for pub in mybd:
                for autor in pub["authors"]:
                    if "affiliation" in autor and autor["affiliation"] and criterio.lower() in autor["affiliation"].lower():
                        resultados.append(pub)
            return resultados
            

        elif escolha == '4':
            criterio = input("Introduza a data de publicação (YYYY-MM-DD):")
            for pub in mybd:
                if "publish_date" in pub and pub["publish_date"] and criterio in pub["publish_date"]:
                    resultados.append(pub)
            return resultados
            
            
        elif escolha == '5':
            criterio = input("Introduza uma palavra-chave: ")
            for pub in mybd:
                if "keywords" in pub and pub["keywords"]:
                    keywords = [kw.strip().lower() for kw in pub["keywords"].split(",")]
                    if criterio.strip().lower() in keywords:
                        resultados.append(pub)
            return resultados        
            

        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 5.")
    
        menu()
        escolha = input("Digite o número do critério que deseja usar: ")

# Listar todos os autores existentes no sistema, bem como as publicações associadas a cada autor
def listar_autores(mybd):
    publicacoes_autores = {}
    for pub in mybd:
        if "title" in pub and pub["title"]:
            titulo = pub["title"]
            for autor in pub["authors"]:
                nome_autor = autor["name"]
                if nome_autor not in publicacoes_autores:
                    publicacoes_autores[nome_autor] = []
                publicacoes_autores[nome_autor].append(titulo)
    
    
    resultados = []
    for autor in sorted (publicacoes_autores.keys (), key=lambda nome: len (publicacoes_autores [nome]),reverse = True) :
        resultados.append (f"Autor: {autor} ({len(publicacoes_autores[autor])} artigo(s))")
        for titulo in publicacoes_autores[autor]:
            resultados.append(f"Publicação: {titulo}")
            resultados.append("")
    return resultados

def menu_distrib():
    menu = """
    Escolha a distribuição que deseja visualizar:
    1) Distribuição de publicações por ano
    2) Distribuição de publicações por mês de um determinado ano
    3) Número de publicações por autor (top 20 autores)
    4) Distribuição de publicações de um autor por anos
    5) Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)
    6) Distribuição de palavras-chave mais frequentes por ano
    0) Sair
    """
    
    print(menu)

# Definição dos gráficos das distribuições
def distrib(mybd):
    menu_distrib()
    escolha = input("Digite o número do critério que deseja usar:")

    while escolha != '0':
        if escolha == "1":
            distribuicao = {}
            for pub in mybd:
                if "publish_date" in pub and pub["publish_date"]:
                    ano = pub["publish_date"][:4]
                    if ano in distribuicao:
                        distribuicao[ano] = distribuicao[ano] + 1
                    else:
                        distribuicao[ano] = 1

            anos = sorted(distribuicao.keys())
            contagens = [distribuicao[ano] for ano in anos]

            plt.figure(figsize=(10,6))
            plt.bar(anos, contagens)
            plt.title("Distribuição de Publicações por Ano", fontsize=14)
            plt.xlabel("Ano", fontsize=12)
            plt.ylabel("Número de Publicações", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        
        elif escolha == "2":
            distribuicao = {}
            ano_determinado = input("Introduza o ano que deseja consultar:")
            for pub in mybd:
                if "publish_date" in pub and pub["publish_date"]:
                    ano = pub["publish_date"][:4]
                    mes = pub["publish_date"][5:7]
                    if ano == ano_determinado:
                        distribuicao[mes] = distribuicao.get(mes,0) + 1

            meses = sorted(distribuicao.keys())
            contagens = [distribuicao[mes] for mes in meses]

            plt.figure(figsize=(10,6))
            plt.bar(meses, contagens)
            plt.title(f"Distribuição de Publicações por Mês em {ano_determinado}", fontsize=14)
            plt.xlabel("Mês", fontsize=12)
            plt.ylabel("Número de Publicações", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif escolha == "3":
            contador_autores= {}
            for pub in mybd:
                if "authors" in pub:
                    for autor in pub["authors"]:
                        autor_nome = autor["name"]
                        if autor_nome in contador_autores:
                            contador_autores[autor_nome] = contador_autores[autor_nome] + 1
                        else:
                            contador_autores[autor_nome] = 1
        
            top_20_autores = sorted(contador_autores.items(), key=lambda x: x[1], reverse=True)[:20]

            autores = [autor[0] for autor in top_20_autores]
            contagens = [autor[1] for autor in top_20_autores]

            plt.figure(figsize=(12, 8))
            plt.barh(autores, contagens, color="skyblue", edgecolor="black")
            plt.gca().invert_yaxis()  
            plt.title("Top 20 Autores com mais Publicações", fontsize=16)
            plt.xlabel("Número de Publicações", fontsize=12)
            plt.ylabel("Autores", fontsize=12)
            plt.tight_layout()
            plt.show()

        elif escolha == "4":
            publicacoes_ano = {}
            autor_nome = input("Introduza o nome do autor que deseja consultar:")
            for pub in mybd:
                if "authors" in pub:
                    for autor in pub["authors"]:
                        if autor["name"] == autor_nome:
                            if "publish_date" in pub:
                                ano_pub = pub["publish_date"][:4]
                                if ano_pub in publicacoes_ano:
                                    publicacoes_ano[ano_pub] = publicacoes_ano[ano_pub] + 1
                                else:
                                    publicacoes_ano[ano_pub] = 1

            anos_ordenados = sorted(publicacoes_ano.items())

            anos = [ano[0] for ano in anos_ordenados]
            quantidade = [ano[1] for ano in anos_ordenados]

            plt.figure(figsize=(10, 6))
            plt.bar(anos, quantidade)
            plt.title(f"Distribuição de Publicações de '{autor_nome}' por Ano", fontsize=16)
            plt.xlabel("Ano", fontsize=12)
            plt.ylabel("Número de Publicações", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif escolha == "5":
            palavras_chave = {}
            for pub in mybd:
                if "keywords" in pub:
                    keywords = pub["keywords"].split(", ")
                    for palavra in keywords:
                        palavra = palavra.lower()
                        if palavra in palavras_chave:
                            palavras_chave[palavra] = palavras_chave[palavra] + 1
                        else:
                            palavras_chave[palavra] = 1

            top_20_palavras = sorted(palavras_chave.items(), key= lambda x: x[1], reverse = True)[:20]

            #if not top_20_palavras:
                #print("Nenhuma palavra-chave encontrada nas publicações.")

            palavras = [item[0] for item in top_20_palavras]
            frequencia = [item[1] for item in top_20_palavras]

            plt.figure(figsize=(10, 6))
            plt.barh(palavras, frequencia)
            plt.gca().invert_yaxis()
            plt.title("Top 20 keywords mais frequentes", fontsize=16)
            plt.xlabel("Frequência", fontsize=12)
            plt.ylabel("Palavras-chave", fontsize=12)
            plt.tight_layout()
            plt.show()
        
        elif escolha == "6":
            ano_desejado = input("Introduza o ano para visualizar a distribuição das palavras-chave:")
            palavras_por_ano = {}
            for pub in mybd:
                if "keywords" in pub and "publish_date" in pub:
                    ano_pub = pub["publish_date"][:4]
                    keywords = pub["keywords"].split(", ")

                    for palavra in keywords:
                        palavra = palavra.lower()
                        if ano_pub not in palavras_por_ano:
                            palavras_por_ano[ano_pub] = {}
                        if palavra in palavras_por_ano[ano_pub]:
                            palavras_por_ano[ano_pub][palavra] = palavras_por_ano[ano_pub][palavra] + 1
                        else:
                            palavras_por_ano[ano_pub][palavra] = 1

            if ano_desejado in palavras_por_ano:
                palavras = palavras_por_ano[ano_desejado]
                palavras_ordenadas = sorted(palavras.items(), key=lambda x: x[1], reverse = True)[:20]
                palavras_frequentes = [p[0] for p in palavras_ordenadas]
                frequencia = [p[1] for p in palavras_ordenadas]
                
            
                plt.figure(figsize=(10, 6))
                plt.barh(palavras_frequentes, frequencia)
                plt.title(f"Top Palavras-chave em {ano_desejado}", fontsize=12)
                plt.xlabel("Frequência", fontsize=10)
                plt.ylabel("Palavras-chave", fontsize=10)
                plt.tight_layout()
                plt.show()
            
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 6.")
    
        menu_distrib()
        escolha = input("Digite o número do critério que deseja usar: ")

# Exportar dados
def exportar_dados(fnome, dados):
    fout = open(fnome, "w", encoding='utf-8')
    json.dump(dados, fout, indent=4, ensure_ascii=False)
    fout.close()

# Mensagem de ajuda
def help():
    help = """
    (1) Carregar o dataset - carrega a informação de um ficheiro para memória.
    (2) Guardar o dataset - guarda a estrutura de dados em memória num ficheiro JSON.
    (3) Inserir um novo registo - insere um novo registo, pedindo critérios como título, abstract, data de publicação, nomes dos autores e suas respetivas afiliações e ORCIDs, palavras-chave, DOI, url e PDF.
    (4) Apagar um registo - apaga um registo, pedindo o DOI desse mesmo registo.
    (5) Consultar um registo - consulta de um registo, pedindo o DOI do registo que quer encontrar.
    (6) Listar os registos - lista um ou vários registos, filtrados por título, autor, afiliação, data de publicação ou palavras-chave.
    (7) Listar autores - lista os autores e os títulos das suas publicações.
    (8) Gráficos de várias distribuições - mostra gráficos de distribuições, como de publicações por ano, de publicações por mês de um determinado ano, do número de publicações por autor (top 20 autores), de publicações de um autor por anos, de palavras-chave pela sua frequência (top 20 palavras-chave) e de palavras-chave mais frequentes por ano.
    (9) Exportar dados para um ficheiro - exporta os dados da última pesquisa para um ficheiro json.
"""
    print(help)