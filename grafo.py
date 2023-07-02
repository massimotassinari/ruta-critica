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

    print(G)
    nx.draw(G, with_labels=True, node_color='lightblue',node_size=500, edge_color='gray')

# Mostrar el grafo
    plt.show()
