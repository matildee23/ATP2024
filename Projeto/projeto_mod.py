import json
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt

# Carregar a informação do dataset para uma estrutura de dados em memória

def carregar_dataset(fnome):
    dataset = []
    try:
        with open(fnome, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        sg.popup(f"Dataset carregado:\nforam lidos {len(dataset)} registos.", 
                title='Sucesso',
                font=('Helvetica', 20))
    except Exception as e: 
        sg.popup(f"Erro ao carregar o dataset: {e}", title='Erro')
    return dataset

# Guardar a estrutura de dados em memória num ficheiro

def guardar_dataset(fnome, dataset):
    try:
        with open(fnome, 'w', encoding='utf-8') as f:
            json.dump(dataset,f, indent=4, ensure_ascii=False)
        sg.popup(f"Dados do ficheiro {fnome} gravados com sucesso.")
    except Exception as e:
        sg.popup(f"Erro ao gravar o dataset: {e}", title='Erro')

# Inserir um novo registo

def inserir_reg(dataset, fnome):
    layout = [
        [sg.Text("Título:"), sg.Input(key="-TITLE-")],
        [sg.Text("Abstract:"), sg.Input(key="-ABSTRACT-")],
        [sg.Text("Palavras-chave (separadas por vírgula):"), sg.Input(key="-KEYWORDS-")],
        [sg.Text("DOI:"), sg.Input(key="-DOI-")],
        [sg.Text("Data de publicação (YYYY-MM-DD):"), sg.Input(key="-DATE-")],
        [sg.Text("PDF:"), sg.Input(key="-PDF-")],
        [sg.Text("Url:"), sg.Input(key="-URL-")],
        [sg.Text("Autores (nomes separados por vírgula):"), sg.Input(key="-AUTHORS-")],
        [sg.Text("Afiliações (separadas por vírgula):"), sg.Input(key="-AFFILIATIONS-")],
        [sg.Text("ORCIDs (caso existam, separados por vírgula):"), sg.Input(key="-ORCIDS-")],
        [sg.Button("Adicionar", key="-ADICIONAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Adicionar novo registo", layout, font=("Helvetica", 14))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-ADICIONAR-":
            title = values["-TITLE-"]
            abstract = values["-ABSTRACT-"]
            keywords = values["-KEYWORDS-"]
            doi = values["-DOI-"]
            publish_date = values["-DATE-"]
            pdf = values["-PDF-"]
            url = values["-URL-"]
            authors_input = values["-AUTHORS-"]
            affiliations_input = values["-AFFILIATIONS-"]
            orcids_input = values["-ORCIDS-"]

            authors = authors_input.split(",")
            affiliations = affiliations_input.split(",")
            orcids = orcids_input.split(",") if orcids_input else []

            if len(authors) < len(affiliations):
                sg.popup("Erro: Número de autores não corresponde ao número de afiliações.", title="Erro")
            else:
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

                duplicado = False
                for registo in dataset:
                    if registo["doi"] == novo_registo["doi"]:
                        duplicado = True
                
                if duplicado:
                    sg.popup("Erro. Esse registo já existe (mesmo DOI).", title="Erro")
                else:
                    dataset.append(novo_registo)
                    sg.popup("Novo registo adicionado com sucesso!", title="Sucesso")

                    stop = True

    window.close()
    return dataset

# Apagar registo

def apagar_reg(dataset):
    layout = [
        [sg.Text("Introduza o DOI do registo que pretende apagar:"), sg.Input(key="-DOI-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Apagar registo",layout,font=("Helvetica", 14))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            doi = values["-DOI-"]
            eliminado = False
            for i, reg in enumerate(dataset):
                if reg["doi"] == doi:
                    del dataset[i]
                    sg.popup(f"Registo com DOI '{doi}' foi apagado.", title="Sucesso")
                    eliminado = True
            if not eliminado:
                sg.popup(f"Registo com DOI '{doi}' não encontrado.", title="Insucesso")

            stop = True

    window.close()
    return dataset

# Consultar registo (com o DOI)

def consultar_reg(dataset):
    layout = [
        [sg.Text("Introduza o DOI da publicação:"), sg.Input(key="-DOI-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Consultar publicação",layout,font=("Helvetica", 14))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            doi = values["-DOI-"]
            reg_encontrado = None
            for reg in dataset:
                if reg["doi"] == doi:
                    sg.popup(f"Registo com DOI '{doi}' encontrado.", title="Sucesso")
                    reg_encontrado = reg
            
            if reg_encontrado == None:
                sg.popup(f"Registo com DOI '{doi}' não encontrado.", title="Insucesso")

            stop = True

    window.close()
    return reg_encontrado

# Listar registos por título

def filtrar_title(dataset):
    layout = [
        [sg.Text("Introduza o título da publicação:"), sg.Input(key="-TITLE-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Filtrar por título",layout,font=("Helvetica", 14))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            title = values["-TITLE-"]
            lista_registos = []
            for pub in dataset:
                if "title" in pub and pub["title"]:
                    if title.lower() == pub["title"].lower():
                        lista_registos.append(pub)
            if lista_registos:
                sg.popup("Registo encontrado", title="Sucesso")
            else:
                sg.popup(f"Registo com título '{title}' não encontrado.", title="Insucesso")

            stop = True
        
    window.close()
    return lista_registos

# Listar registos por data

def filtrar_date(dataset):
    layout = [
        [sg.Text("Introduza a data de publicação (YYYY-MM-DD):"), sg.Input(key="-DATE-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Filtrar por data de publicação",layout,font=("Helvetica", 14))

    stop = False
    lista_registos = []
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            date = values["-DATE-"]
            for reg in dataset:
                if "publish_date" in reg and reg["publish_date"] and date in reg["publish_date"]:
                    lista_registos.append(reg)
            if lista_registos:
                sg.popup(f"{len(lista_registos)} registo(s) encontrado(s).", title="Sucesso")
            else:
                sg.popup(f"Registo com data de publicação '{date}' não encontrado.", title="Insucesso")

            stop = True
        
    window.close()
    return lista_registos

# Listar registos por autor

def filtrar_author(dataset):
    layout = [
        [sg.Text("Introduza o nome do autor:"), sg.Input(key="-AUTHOR-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Filtrar por nome do autor",layout,font=("Helvetica", 14))

    stop = False
    lista_registos = []
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            author = values["-AUTHOR-"]
            for reg in dataset:
                for autor in reg["authors"]:
                    if author == autor["name"]:
                        lista_registos.append(reg)
            if lista_registos:
                sg.popup(f"{len(lista_registos)} registo(s) encontrado(s).", title="Sucesso")
            else:
                sg.popup(f"Registo com nome '{author}' não encontrado.", title="Insucesso")

            stop = True
        
    window.close()
    return lista_registos

# Listar registos por keywords

def filtrar_keywords(dataset):
    layout = [
        [sg.Text("Introduza uma palavra-chave:"), sg.Input(key="-KEYWORD-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Filtrar por palavra-chave",layout,font=("Helvetica", 14))

    stop = False
    lista_registos = []
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            keyword = values["-KEYWORD-"]
            for reg in dataset:
                if "keywords" in reg and reg["keywords"]:
                    keywords = [kw.strip().lower() for kw in reg["keywords"].split(",")]
                    if keyword.strip().lower() in keywords:
                        lista_registos.append(reg)
            if lista_registos:
                sg.popup(f"{len(lista_registos)} registo(s) encontrado(s).", title="Sucesso")
            else:
                sg.popup(f"Registo com palavra-chave '{keyword}' não encontrado.", title="Insucesso")

            stop = True
        
    window.close()
    return lista_registos

# Listar registos por afiliação

def filtrar_affiliations(dataset):
    layout = [
        [sg.Text("Introduza a afiliação:"), sg.Input(key="-AFFILIATION-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    window = sg.Window("Filtrar por afiliação",layout,font=("Helvetica", 14))

    stop = False
    lista_registos = []
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            affiliation = values["-AFFILIATION-"]
            for reg in dataset:
                for autor in reg["authors"]:
                    if "affiliation" in autor and autor["affiliation"] and affiliation.lower() in autor["affiliation"].lower():
                        lista_registos.append(reg)
            if lista_registos:
                sg.popup(f"{len(lista_registos)} registo(s) encontrado(s).", title="Sucesso")
            else:
                sg.popup(f"Registo com afiliação '{affiliation}' não encontrado.", title="Insucesso")

            stop = True
        
    window.close()
    return lista_registos

def menu_filtros(dataset):
    layout = [
        [sg.Button("Por título", key="-TITLE-")],
        [sg.Button("Por data de publicação", key="-DATE-")],
        [sg.Button("Por autor", key="-AUTHOR-")],
        [sg.Button("Por palavra-chave", key="-KEYWORD-")],
        [sg.Button("Por afiliação", key="-AFFILIATION-")],
        [sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Escolher filtro",layout,font=("Helvetica", 14))

    resultado = None
    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-TITLE-":
            resultado = filtrar_title(dataset)
            if resultado:
                stop = True
        elif event == "-DATE-":
            resultado = filtrar_date(dataset)
            if resultado:
                stop = True
        elif event == "-AUTHOR-":
            resultado = filtrar_author(dataset)
            if resultado:
                stop = True
        elif event == "-KEYWORD-":
            resultado = filtrar_keywords(dataset)
            if resultado:
                stop = True
        elif event == "-AFFILIATION-":
            resultado = filtrar_affiliations(dataset)
            if resultado:
                stop = True
    window.close()
    return resultado

def listar_autores(dataset):
    publicacoes_autores = {}
    for pub in dataset:
        if "title" in pub and pub["title"]:
            titulo = pub["title"]
            for autor in pub["authors"]:
                nome_autor = autor["name"]
                if nome_autor not in publicacoes_autores:
                    publicacoes_autores[nome_autor] = []
                publicacoes_autores[nome_autor].append(titulo)
        
    resultado = []
    for autor in sorted(publicacoes_autores.keys(), key=lambda nome: len(publicacoes_autores[nome]), reverse = True):
        resultado.append(f"Autor: {autor}  ({len(publicacoes_autores[autor])} artigo(s))")
        for titulo in publicacoes_autores[autor]:
            resultado.append(f"  Publicação: {titulo}")
            resultado.append("")

    return resultado

def distrib_porano(dataset):
    distribuicao = {}
    for pub in dataset:
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

def distrib_pormes_ano(dataset):
    layout = [
        [sg.Text("Introduza um ano:"), sg.Input(key="-ANO-")],
        [sg.Button("Gráfico", key="-GRAFICO-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    window = sg.Window("Distribuição de publicações por mês num determinado ano",layout,font=("Helvetica", 14))

    stop = False
    distribuicao = {}
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-GRAFICO-":
            ano_determinado = values["-ANO-"]
            for pub in dataset:
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

def top_autores(dataset):
    contador_autores= {}
    for pub in dataset:
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

def publi_autor(dataset):
    layout = [
        [sg.Text("Introduza o nome do autor:"), sg.Input(key="-AUTOR-")],
        [sg.Button("Gráfico", key="-GRAFICO-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    window = sg.Window("Distribuição de publicações de um autor por ano",layout,font=("Helvetica", 14))

    stop = False
    publicacoes_ano = {}
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-GRAFICO-":
            autor_nome = values["-AUTOR-"]
            for pub in dataset:
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

def top_keywords(dataset):
    palavras_chave = {}
    for pub in dataset:
        if "keywords" in pub:
            keywords = pub["keywords"].split(", ")
            for palavra in keywords:
                palavra = palavra.lower()
                if palavra in palavras_chave:
                    palavras_chave[palavra] = palavras_chave[palavra] + 1
                else:
                    palavras_chave[palavra] = 1

    top_20_palavras = sorted(palavras_chave.items(), key= lambda x: x[1], reverse = True)[:20]

    if not top_20_palavras:
        sg.popup("Nenhuma palavra-chave encontrada nas publicações.", title="Insucesso")

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

def distrib_keyano(dataset):
    layout = [
        [sg.Text("Introduza o ano:"), sg.Input(key="-ANO-")],
        [sg.Button("Gráfico", key="-GRAFICO-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]
    
    window = sg.Window("Distribuição de palavras-chave mais frequentes por ano",layout,font=("Helvetica", 14))

    stop = False
    palavras_por_ano = {}
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-GRAFICO-":
            ano_desejado = values["-ANO-"]
            for pub in dataset:
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

def menu_grafs(dataset):
    layout = [
        [sg.Button("Distribuição de publicações por ano", key="-PORANO-")],
        [sg.Button("Distribuição de publicações por mês de um determinado ano", key="-PORMES-")],
        [sg.Button("Top 20 autores com mais publicações", key="-TOPAUTORES-")],
        [sg.Button("Distribuição de publicações de um autor por ano", key="-AUTORPORANO-")],
        [sg.Button("Top 20 keywords mais frequentes", key="-TOPKEYWORDS-")],
        [sg.Button("Distribuição de palavras-chave mais frequentes por ano", key="-KEYWORDSANO-")],
        [sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Gráficos de estatísticas de publicação",layout,font=("Helvetica", 14))

    resultado = None
    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-PORANO-":
            resultado = distrib_porano(dataset)
            if resultado:
                stop = True
        elif event == "-PORMES-":
            resultado = distrib_pormes_ano(dataset)
            if resultado:
                stop = True
        elif event == "-TOPAUTORES-":
            resultado = top_autores(dataset)
            if resultado:
                stop = True
        elif event == "-AUTORPORANO-":
            resultado = publi_autor(dataset)
            if resultado:
                stop = True
        elif event == "-TOPKEYWORDS-":
            resultado = top_keywords(dataset)
            if resultado:
                stop = True
        elif event == "-KEYWORDSANO-":
            resultado = distrib_keyano(dataset)
            if resultado:
                stop = True

    window.close()
    return resultado

def exportar_dados(dados):
    layout = [
        [sg.Text("Introduza um nome para o ficheiro (nome.json) para qual pretende exportar os dados:"), sg.Input(key="-FICHEIRO-")],
        [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")]
    ]

    window = sg.Window("Exportação de dados para um ficheiro",layout,font=("Helvetica", 14))

    stop = False
    while not stop:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop = True
        elif event == "-CONFIRMAR-":
            fnome = values["-FICHEIRO-"]
            if fnome:
                try:
                    with open(fnome, "w", encoding='utf-8') as f:
                        json.dump(dados, f, indent=4, ensure_ascii=False)
                    sg.popup(f"Dados exportados com sucesso.")
                except Exception as e:
                    sg.popup(f"Erro ao exportar dados: {e}", title='Erro')