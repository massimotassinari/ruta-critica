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

    print(G)
    nx.draw(G, with_labels=True, node_color='lightblue',
            node_size=500, edge_color='gray')

# Mostrar el grafo
    plt.show()
