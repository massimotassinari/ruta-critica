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

    color_map = []
    for node in G.nodes():
        G.nodes[node]['pos_asign'] = False
        if G.nodes[node]['H'] == 0:
            color_map.append(('#6e46c4'))
        else:
            color_map.append(('#e691ca'))

    # Establecer posición de los nodos
    for node in G.nodes():
        if G.nodes[node] == start_node:
            G.nodes[node]['pos_asign'] = True
        acum_y = 0
        for sucesor in list(G.nodes[node]['sucesor']):
            if G.nodes[sucesor]['pos_asign'] == False:
                G.nodes[sucesor]['posx'] = G.nodes[node]['posx'] + 2
                G.nodes[sucesor]['posy'] = G.nodes[node]['posy'] - acum_y
                G.nodes[sucesor]['pos'] = (G.nodes[sucesor]['posx'], G.nodes[sucesor]['posy'])
                acum_y = acum_y + 0.5
                G.nodes[sucesor]['pos_asign'] = True


    # Obtener posición de los nodos del grafo
    pos = nx.get_node_attributes(G,'pos')

    options_arrow = {
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 15,
    }

    dias = []
    for i in range(G.nodes[start_node]['ES'], G.nodes[finish_node]['EF']):
        dia = 'día ' + str(i)
        dias.append(dia)

    mapeado = range(len(dias))

    # Configurar la forma de dibujar el grafo
    image_file = "ruta-critica/fondografo.png"
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_facecolor('#d4b7ff')
    nx.draw_networkx_nodes(G, pos, node_color = color_map, node_size=500)
    nx.draw_networkx_edges(G, pos, alpha=0.6, edge_color='black', arrows=True, **options_arrow)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
    plt.xticks(mapeado, dias) 
    plt.title('Actividades de la Ruta Crítica (Nodos en Morado)')
    plt.show()

    return G, critical_path
