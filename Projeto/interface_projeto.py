import FreeSimpleGUI as sg
import projeto_mod as proj
import json

# Layout da interface
menu_layout = [ 
    [sg.Button("Carregar", key='-CARREGAR-')],
    [sg.Button("Guardar", key='-GUARDAR-')],
    [sg.Button("Inserir", key='-INSERIR-')],
    [sg.Button("Apagar", key='-APAGAR-')],
    [sg.Button("Consultar um registo", key='-CONSULTAR-')],
    [sg.Button("Filtrar", key='-FILTRAR-')],
    [sg.Button("Listar autores", key='-LISTAR-')],
    [sg.Button("Estatísticas de publicação", key='-GRAFICOS-')],
    [sg.Button("Exportar dados", key='-EXPORTAR-')],
    [sg.Multiline(size=(50,10), key='-DADOS-')],
    [sg.Button("Sair", key='-SAIR-')]
]

# Tema de cores
sg.theme('Kayak')

# Janela principal
window = sg.Window("Sistema de Consulta e Análise de Publicações científicas", menu_layout, font=("Helvetica", 24))

# Event listener
dataset = []
resultado = []
stop = False
while not stop:
    event, values = window.read()
    if event in [sg.WINDOW_CLOSED, '-SAIR-']:
        stop = True
    elif event == '-CARREGAR-':
        ficheiro =sg.popup_get_file("Selecione o ficheiro JSON",
                                    file_types=(("Ficheiros JSON", "*.json"),))
        if ficheiro:
            dataset = proj.carregar_dataset(ficheiro)
    elif event == '-GUARDAR-':
        if ficheiro:
            proj.guardar_dataset(ficheiro, dataset)
    elif event == '-INSERIR-':
        dataset = proj.inserir_reg(dataset, ficheiro)
        if dataset:
            window["-DADOS-"].update(json.dumps(dataset, indent=4, ensure_ascii=False))
    elif event == '-APAGAR-':
        dataset = proj.apagar_reg(dataset)
        if dataset:
            window["-DADOS-"].update(json.dumps(dataset, indent=4, ensure_ascii=False))
    elif event == '-CONSULTAR-':
        resultado = proj.consultar_reg(dataset)
        if resultado:
            window["-DADOS-"].update(json.dumps(resultado, indent=4, ensure_ascii=False))
    elif event == '-FILTRAR-':
        resultado = proj.menu_filtros(dataset)
        if resultado:
            window["-DADOS-"].update(json.dumps(resultado, indent=4, ensure_ascii=False))
    elif event == '-LISTAR-':
        resultado = proj.listar_autores(dataset)
        if resultado:
            window["-DADOS-"].update(json.dumps(resultado, indent=4, ensure_ascii=False))
    elif event == '-GRAFICOS-':
        proj.menu_grafs(dataset)
    elif event == '-EXPORTAR-':
        if resultado:
            proj.exportar_dados(resultado)
        else:
            sg.popup("Não há dados para exportar.", title="Insucesso")
window.close()