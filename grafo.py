import networkx as nx
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import tkinter
import funciones as f


# Función para correr el CPM
def runCPM(info):
    # Creación del grafo
    G = nx.DiGraph()
    # Nodo de inicio
    for act in info:
        if act['start_node'] == True:
            start_node = act['ID']
        if act['finish_node'] == True:
            finish_node = act['ID']

# Se agregan los nodos al grafo
    for item in info:
        # Agregamos el nodo al grafo
        G.add_node(item['ID'], pos=(0, 0))

        # Asignamos atributos al nodo creado
        G.nodes[item['ID']]['ID'] = item['ID']
        G.nodes[item['ID']]['descripcion'] = item['descripcion']
        G.nodes[item['ID']]['start_node'] = item['start_node']
        G.nodes[item['ID']]['finish_node'] = item['finish_node']

        # Teniendo una lista de sucesores y predecesores por nodo, podemos aplicar ForwardPass y BacwardPass
        # en el algoritmo de la ruta crítica
        G.nodes[item['ID']]['predecesor'] = item['predecesor']
        G.nodes[item['ID']]['sucesor'] = []

        # Asignamos los atributos que nos permitirán encontrar la ruta crítica
        # Corresponde a la duración de la actividad
        G.nodes[item['ID']]['D'] = item['duracion']
        # Corresponde al Early Start (Inicio más temprano)
        G.nodes[item['ID']]['ES'] = 0
        # Corresponde al Early Finish (Inicio más tardío)
        G.nodes[item['ID']]['EF'] = 0
        # Corresponde al Late Start (Culminación más temprana)
        G.nodes[item['ID']]['LS'] = 0
        # Corresponde al Late Finish (Culminación más tardía)
        G.nodes[item['ID']]['LF'] = math.inf
        # Corresponde a la Holgura de la actividad
        G.nodes[item['ID']]['H'] = 0
        G.nodes[item['ID']]['posx'] = 0
        G.nodes[item['ID']]['posy'] = 0

    # Se agregan las aristas al grafo y se crean los sucesores de cada nodo
    for node in G.nodes():
        if G.nodes[node]['predecesor'] != None:
            for predecesor in G.nodes[node]['predecesor']:
                G.add_edge(predecesor, node, weight=G.nodes[predecesor]['D'])
                # Al nodo predecesor le asignamos su sucesor
                G.nodes[predecesor]['sucesor'].append(G.nodes[node]['ID'])

    # Iniciamos el algoritmo de la ruta crítica

    # Primero aplicamos el ForwardPass, donde usaremos la lista de actividades sucesoras que hay en cada actividad
    for node in G.nodes():

        G.nodes[node]['EF'] = G.nodes[node]['ES'] + G.nodes[node]['D']

        for sucesor in list(G.nodes[node]['sucesor']):
            if G.nodes[node]['EF'] > G.nodes[sucesor]['ES']:
                G.nodes[sucesor]['ES'] = G.nodes[node]['EF']
                G.nodes[sucesor]['EF'] = G.nodes[sucesor]['ES'] + \
                    G.nodes[sucesor]['D']

        if G.nodes[node]['predecesor'] != None:
            for predecesor in list(G.nodes[node]['predecesor']):
                if G.nodes[predecesor]['EF'] > G.nodes[node]['ES']:
                    G.nodes[node]['ES'] = G.nodes[predecesor]['EF']
                    G.nodes[node]['EF'] = G.nodes[node]['ES'] + \
                        G.nodes[node]['D']

        if G.nodes[node]['finish_node'] == True:
            G.nodes[node]['LF'] = G.nodes[node]['EF']

        # Ahora aplicamos el BackwardPass, donde usaremos la lista de actividades predecesoras que hay en cada actividad
    while G.nodes[start_node]['start_node'] != False:

        for node in G.nodes():
            if G.nodes[node]['finish_node'] == True:

                G.nodes[node]['LS'] = G.nodes[node]['LF'] - G.nodes[node]['D']
                G.nodes[node]['finish_node'] = False

                if G.nodes[node]['predecesor'] != None:
                    for predecesor in list(G.nodes[node]['predecesor']):
                        if G.nodes[node]['LS'] < G.nodes[predecesor]['LF']:
                            G.nodes[predecesor]['LF'] = G.nodes[node]['LS']
                            G.nodes[predecesor]['LS'] = G.nodes[predecesor]['LF'] - \
                                G.nodes[predecesor]['D']
                        G.nodes[predecesor]['finish_node'] = True

                if G.nodes[node] == G.nodes[start_node]:
                    G.nodes[node]['start_node'] = False

    # Calculo de la holgura de cada actividad
    for node in G.nodes():
        G.nodes[node]['H'] = G.nodes[node]['LS'] - G.nodes[node]['ES']

    # Obtener camíno de la ruta crítica en orden
    critical_path = []
    inicio_CP = start_node
    # print(str(inicio_CP))
    critical_path.append(inicio_CP)

    while G.nodes[inicio_CP] != G.nodes[finish_node]:
        for sucesor in list(G.nodes[inicio_CP]['sucesor']):
            if G.nodes[sucesor]['H'] == 0:
                inicio_CP = G.nodes[sucesor]['ID']
                critical_path.append(inicio_CP)

    ########
    window = tkinter.Tk()
    window.geometry("1024x600")
    window.wm_title("Problema Ruta Crítica")

    # Título del Reporte
    label_act = tkinter.Label(window, fg="#a60338", text="Reporte de Actividades (Ejemplo del Parcial 2)", font=(
        "verdana", 12)).place(x=190, y=15)

    # Terminos a tomar en consideración
    terminos = tkinter.Label(window, fg="#a60338", text="Terminos usados en el reporte", font=(
        "verdana", 10)).place(x=790, y=70)
    termino_D = tkinter.Label(window, fg="#2d2da7", text="D: Duración", font=(
        "verdana", 10)).place(x=790, y=100)
    termino_ES = tkinter.Label(window, fg="#2d2da7", text="ES:", font=(
        "verdana", 10)).place(x=790, y=130)
    termino_ES1 = tkinter.Label(window, fg="#2d2da7", text="Early Start (Inicio más temprano)", font=(
        "verdana", 7)).place(x=820, y=130)
    termino_EF = tkinter.Label(window, fg="#2d2da7", text="EF:", font=(
        "verdana", 10)).place(x=790, y=160)
    termino_EF1 = tkinter.Label(window, fg="#2d2da7", text="Early Finish (Inicio más tardío)", font=(
        "verdana", 7)).place(x=820, y=160)
    termino_LS = tkinter.Label(window, fg="#2d2da7", text="LS:", font=(
        "verdana", 10)).place(x=790, y=190)
    termino_LS1 = tkinter.Label(window, fg="#2d2da7", text="Late Start (Culminación más temprana)", font=(
        "verdana", 7)).place(x=820, y=190)
    termino_LF = tkinter.Label(window, fg="#2d2da7", text="LF:", font=(
        "verdana", 10)).place(x=790, y=220)
    termino_LF1 = tkinter.Label(window, fg="#2d2da7", text="Late Finish (Culminación más tardía)", font=(
        "verdana", 7)).place(x=820, y=220)
    termino_H = tkinter.Label(window, fg="#2d2da7", text="H: Holgura", font=(
        "verdana", 10)).place(x=790, y=250)

    # Etiquetas cuadro del reporte
    label_act = tkinter.Label(window, fg="#2d2da7", text="| Actividad", font=(
        "verdana", 10)).place(x=20, y=50)
    label_des = tkinter.Label(window, fg="#2d2da7", text="| Descripción", font=(
        "verdana", 10)).place(x=100, y=50)
    label_pre = tkinter.Label(window, fg="#2d2da7", text="| Predecesor", font=(
        "verdana", 10)).place(x=220, y=50)
    label_suc = tkinter.Label(window, fg="#2d2da7", text="| Sucesor", font=(
        "verdana", 10)).place(x=320, y=50)
    label_D = tkinter.Label(window, fg="#2d2da7", text="| D", font=(
        "verdana", 10)).place(x=420, y=50)
    label_ES = tkinter.Label(window, fg="#2d2da7", text="| ES", font=(
        "verdana", 10)).place(x=480, y=50)
    label_EF = tkinter.Label(window, fg="#2d2da7", text="| EF", font=(
        "verdana", 10)).place(x=540, y=50)
    label_LS = tkinter.Label(window, fg="#2d2da7", text="| LS", font=(
        "verdana", 10)).place(x=600, y=50)
    label_LF = tkinter.Label(window, fg="#2d2da7", text="| LF", font=(
        "verdana", 10)).place(x=660, y=50)
    label_H = tkinter.Label(window, fg="#2d2da7", text="| H", font=(
        "verdana", 10)).place(x=720, y=50)

    # Cada registro completa de cada actividad
    pos_y = 50
    aux_predecesor = {}
    aux_sucesor = {}
    for node in G.nodes():
        pos_y += 50
        if G.nodes[node]['predecesor'] == None:
            aux_predecesor = '--'
        else:
            aux_predecesor = str(G.nodes[node]['predecesor'])
        if len(G.nodes[node]['sucesor']) == 0:
            aux_sucesor = '--'
        else:
            aux_sucesor = str(G.nodes[node]['sucesor'])

        tkinter.Label(window, fg="#292931", text="| " +
                      str(node), font=("verdana", 10)).place(x=20, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['descripcion']), font=("verdana", 7)).place(x=100, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + aux_predecesor,
                      font=("verdana", 10)).place(x=220, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + aux_sucesor,
                      font=("verdana", 10)).place(x=320, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['D']) + " días", font=("verdana", 10)).place(x=420, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['ES']) + " días", font=("verdana", 10)).place(x=480, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['EF']) + " días", font=("verdana", 10)).place(x=540, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['LS']) + " días", font=("verdana", 10)).place(x=600, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['LF']) + " días", font=("verdana", 10)).place(x=660, y=pos_y)
        tkinter.Label(window, fg="#292931", text="| " + str(
            G.nodes[node]['H']) + " días", font=("verdana", 10)).place(x=720, y=pos_y)

    pos_y += 50

    text1 = 'NOTA: Las actividades que forman parte de la ruta crítica son aquellas que tienen holgura "H" igual a 0) y, por lo tanto, no se pueden retrasar ya que afectarían la ejecución del proyecto. '
    text2 = 'Por otro lado, aquellas que tienen holgura "H" mayor a 0 pueden retrasarse un poco sin afectar al proyecto en general. '
    text3 = 'A continuación se muestran las actividades de la ruta crítica en un arreglo en orden de éjecución: ' + \
            str(critical_path)
    show_text = text1 + text2 + text3
    label_CP = tkinter.Label(window, fg='#034f0c', text=show_text, wraplength=600, font=(
        "verdana", 10)).place(x=20, y=pos_y)

    text4 = 'Puede observar mejor las actividades de la ruta crítica viendo el grafo. Para ello presione en el botón de abajo "Mostrar Grafo de la Ruta Crítica"'
    label_btn_mostrar_grafo = label_CP = tkinter.Label(
        window, fg='#960019', text=text4, wraplength=200, font=("verdana", 10)).place(x=800, y=400)
    btn_mostrar_grafo_CP = tkinter.Button(
        window, bg='#d15b70', text="Mostrar Grafo de la Ruta Crítica", command=mostrar_grafo, font=("verdana", 10)).place(x=780, y=500)

    window.mainloop()

    #######

    print(G)
    nx.draw(G, with_labels=True, node_color='lightblue',node_size=500, edge_color='gray')

# Mostrar el grafo
    plt.show()
