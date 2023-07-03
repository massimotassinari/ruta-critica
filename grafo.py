import networkx as nx
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import tkinter
import funciones as f


# Funcion que corre la Ruta critica CPM
def runCPM(info):
    # Se crea el grafo (Vacio) con el modulo networkx
    G = nx.DiGraph()
    # Se identifican el nodo inicio y el nodo fin
    for act in info:
        if act['start_node'] == True:
            start_node = act['ID']
        if act['finish_node'] == True:
            finish_node = act['ID']

# Se agregan los nodos al grafo creado "G"
    for item in info:
        # Se agrega el nodo vacio
        G.add_node(item['ID'], pos=(0, 0))

        # Se asignan los distintos atributos al nodo (ID, descripcion,nodo inicio, nodo fin, lista de predecesores, lista de sucesores)
        G.nodes[item['ID']]['ID'] = item['ID']
        G.nodes[item['ID']]['descripcion'] = item['descripcion']
        G.nodes[item['ID']]['start_node'] = item['start_node']
        G.nodes[item['ID']]['finish_node'] = item['finish_node']

        # Con estas listas aplicamos el forward pass y backward pass
        G.nodes[item['ID']]['predecesor'] = item['predecesor']
        G.nodes[item['ID']]['sucesor'] = []

        # Se añaden los atributos que haran presencia en la ruta critica

        G.nodes[item['ID']]['D'] = item['duracion']  # Duracion de actividad

        G.nodes[item['ID']]['ES'] = 0  # Early Start (Inicio más temprano)

        G.nodes[item['ID']]['EF'] = 0  # Early Finish (Inicio más tardío)

        G.nodes[item['ID']]['LS'] = 0  # Late Start (Culminación más temprana)

        # Late Finish (Culminación más tardía) predeterminado como infinito usando la libreria "math"
        G.nodes[item['ID']]['LF'] = math.inf

        G.nodes[item['ID']]['H'] = 0    # Holgura de la actividad
        # Ayudara a la ubivacion del eje x en las etiquetas de la ventana que muestra la tabla
        G.nodes[item['ID']]['posx'] = 0
        # Ayudara a la ubivacion del eje y en las etiquetas de la ventana que muestra la tabla
        G.nodes[item['ID']]['posy'] = 0

    # Agregamos las aristas al grafo
    for node in G.nodes():
        if G.nodes[node]['predecesor'] != None:
            for predecesor in G.nodes[node]['predecesor']:
                G.add_edge(predecesor, node, weight=G.nodes[predecesor]['D'])
                # Le asignamos el sucesor al nodo predecesor
                G.nodes[predecesor]['sucesor'].append(G.nodes[node]['ID'])

    """Se inicia el algoritmo de ruta critica"""

    """ForwardPass"""
    # Se usa la lista sucesores de cada actividad
    for node in G.nodes():

        # Se hace la suma de ES + D para obtener el EF la actividad
        G.nodes[node]['EF'] = G.nodes[node]['ES'] + G.nodes[node]['D']

        for sucesor in list(G.nodes[node]['sucesor']):
            # Se buscan los sucesores de la actividad y se actializa su ES, si una actividad ya lo tiene se compueba que esta sea mayor si no se modifica para obtener el timepo mas lejano
            if G.nodes[node]['EF'] > G.nodes[sucesor]['ES']:
                # Se modifica el EF del sucesor de la actividad que estamos evaluando si esta es menor, asi como su EF
                G.nodes[sucesor]['ES'] = G.nodes[node]['EF']
                G.nodes[sucesor]['EF'] = G.nodes[sucesor]['ES'] + \
                    G.nodes[sucesor]['D']

        if G.nodes[node]['predecesor'] != None:

            for predecesor in list(G.nodes[node]['predecesor']):
                # Verifica que el EF de los predecesores de la actividad evaluando no sean mayores a los de la actividad que se esta evaluando
                if G.nodes[predecesor]['EF'] > G.nodes[node]['ES']:
                    G.nodes[node]['ES'] = G.nodes[predecesor]['EF']
                    G.nodes[node]['EF'] = G.nodes[node]['ES'] + \
                        G.nodes[node]['D']

        if G.nodes[node]['finish_node'] == True:
            # Aqui para la actividad final pone el atributo de LF igual al del EF, para empezar el backward

            G.nodes[node]['LF'] = G.nodes[node]['EF']

    """BackwardPass"""
    # Se usa la lista de actividades predecesoras que hay en cada actividad
    while G.nodes[start_node]['start_node'] != False:

        for node in G.nodes():
            # Se encuentra el nodo final para empezar
            if G.nodes[node]['finish_node'] == True:
                # Se calcula su LS a partir del LF - duracion

                G.nodes[node]['LS'] = G.nodes[node]['LF'] - G.nodes[node]['D']
                # Se cambia el atributo finish node para no ser tomado en cuenta nuevamente
                G.nodes[node]['finish_node'] = False

                if G.nodes[node]['predecesor'] != None:
                    # Si hay predecesores entonces se itera sobre ellos
                    for predecesor in list(G.nodes[node]['predecesor']):
                        # Si el LF del predecesor es mayor al LS de la actividad actual se actualiza el LS y el LF del predecesor para que sea el menor
                        if G.nodes[node]['LS'] < G.nodes[predecesor]['LF']:
                            G.nodes[predecesor]['LF'] = G.nodes[node]['LS']
                            G.nodes[predecesor]['LS'] = G.nodes[predecesor]['LF'] - \
                                G.nodes[predecesor]['D']

                        # Se cambia su atributo Finish node a True para que sea tomado en cuenta en la proxima iteracion
                        G.nodes[predecesor]['finish_node'] = True

                # Si llega al nodo inicio vuelve a cambiar su Start node a False par que no siga iterando el while
                if G.nodes[node] == G.nodes[start_node]:
                    G.nodes[node]['start_node'] = False

    # Se calcula la holgura de cada actividad LS - ES
    for node in G.nodes():
        G.nodes[node]['H'] = G.nodes[node]['LS'] - G.nodes[node]['ES']

    # Se obtiene la ruta critica en el orden adecuado
    critical_path = []
    inicio_CP = start_node
    critical_path.append(inicio_CP)

    while G.nodes[inicio_CP] != G.nodes[finish_node]:
        for sucesor in list(G.nodes[inicio_CP]['sucesor']):
            # Si tiene una holgura 0 se toma en cuenta y se agrega a la lista, tambien cambia la variable de inicioCp para que busque el siguiente
            if G.nodes[sucesor]['H'] == 0:
                inicio_CP = G.nodes[sucesor]['ID']
                critical_path.append(inicio_CP)

    return G, critical_path, start_node,finish_node



    
