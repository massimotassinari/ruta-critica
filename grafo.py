import networkx as nx
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import tkinter
import funciones as f
# descripción del problema:
# Ud. desea remodelar el baño de su habitación, y los contratistas le han indicado que ello
# conlleva las siguientes actividades:

# Identif.	 Descripción	           Duración	      Requisito
#  A	     Quitar cerámicas	       2		      --
#  B	     Instalar cableado	       3		      A
#  C	     Instalar calentador       1		      B,E
#  D	     Instalar bomba	           3		      E
#  E		 Instalar Tuberías	       2		      A
#  F		 Instalar Jacuzzi	       2		      C,D
#  G		 Pruebas y Ajustes         2		      F

# Se requiere construir un programa que lea los datos de unas actividades
# (identificación, descripción, duración y predecesores)  a fin de aplicar
# el algoritmo de la Ruta Crítica al grafo resultante y producir un reporte
# de actividades indicando las fechas más tempranas y más tardías de inicio
# y de terminación, indicando cuáles están en la ruta crítica y cuales tienen holgura.


# Definición del arreglo con la información de las actividades
info = [
    {'ID': 'A', 'descripcion': 'Quitar cerámicas', 'duracion': 2,
        'predecesor': None, 'start_node': False, 'finish_node': False},
    {'ID': 'B', 'descripcion': 'Instalar cableado', 'duracion': 3,
     'predecesor': ['A'], 'start_node':False, 'finish_node':False},
    {'ID': 'C', 'descripcion': 'Instalar calentador', 'duracion': 1,
        'predecesor': ['B', 'E'], 'start_node':False, 'finish_node':False},
    {'ID': 'D', 'descripcion': 'Instalar bomba', 'duracion': 3,
     'predecesor': ['E'], 'start_node':False, 'finish_node':False},
    {'ID': 'E', 'descripcion': 'Instalar tuberías', 'duracion': 2,
     'predecesor': ['A'], 'start_node':False, 'finish_node':False},
    {'ID': 'F', 'descripcion': 'Instalar jacuzzi', 'duracion': 2,
        'predecesor': ['C', 'D'], 'start_node':False, 'finish_node':False},
    {'ID': 'G', 'descripcion': 'Pruebas y ajustes', 'duracion': 2,
        'predecesor': ['F'], 'start_node':False, 'finish_node':False}
]

# Buscar inicio y fin


info = f.start_finish_nodes(info)

# Creación del grafo
G = nx.DiGraph()

# Función para correr el CPM


def runCPM(info):
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
                    G.add_edge(predecesor, node,
                               weight=G.nodes[predecesor]['D'])

                    # Al nodo predecesor le asignamos su sucesor
                    G.nodes[predecesor]['sucesor'].append(G.nodes[node]['ID'])

    print(G)


runCPM(info)
