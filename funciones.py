
def start_finish_nodes(info):
    '''
    info ==> lista de diccionarios donde cada diccionario es una actividad
    return ==> retorna la lista info actualizada con los parametros de start node y finish node en True
    '''
    actividades = []
    predecesoras = []

    for actividad in info:
        actividades.append(actividad['ID'])
        try:
            for predecesor in actividad['predecesor']:
                if predecesor not in predecesoras:
                    predecesoras.append(predecesor)
        except Exception:
            print("ERROR! No hay predecesores")

        if actividad['predecesor'] == ['']:
            actividad['start_node'] = True
            actividad['predecesor'] = None

    finish_node = [
        elemento for elemento in actividades if elemento not in predecesoras]  # lambda function que devuelve una lista de los ID de la actividas que no tiene sucesor

    for actividad in info:
        if actividad['ID'] == finish_node[0]:
            # Cambia el atributo de la actividad que es nodo final
            actividad['finish_node'] = True

    return info
