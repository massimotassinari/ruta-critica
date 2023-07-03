
def start_finish_nodes(info):
    '''
    info ==> lista de diccionarios donde cada diccionario es una actividad
    return ==> retorna la lista info actualizada con los parametros de start node y finish node en True
    '''
    actividades = []
    predecesoras = []

    contar =0

    for actividad in info:
        actividades.append(actividad['ID'])
        try:
            for predecesor in actividad['predecesor']:
                if predecesor not in predecesoras:
                    predecesoras.append(predecesor)
        except Exception:
            print("ERROR! No hay predecesores")

        if actividad['predecesor'] == ['']:
            contar +=1
          
            actividad['start_node'] = True
            actividad['predecesor'] = None

    finish_node = [
        elemento for elemento in actividades if elemento not in predecesoras]  # lambda function que devuelve una lista de los ID de la actividas que no tiene sucesor
    count = 0
    for actividad in info:
        for x in finish_node:
            if actividad['ID'] == x:
                # Cambia el atributo de la actividad que es nodo final
                actividad['finish_node'] = True
                count += 1
    if count > 1:
        for y in info:
            if y['finish_node'] == True:
                y['finish_node'] = False
        info.append({'ID': 'Z', 'descripcion': 'Final', 'duracion': 0,
                    'predecesor': finish_node, 'start_node': False, 'finish_node': True})
    #inicio
    
    
    if count > 1:
        for y in info:
            if y['start_node'] == True:
                y['start_node'] = False
                y['predecesor'] = ['@']
        info.append({'ID': '@', 'descripcion': 'Inicio', 'duracion': 0,
                    'predecesor': None, 'start_node': True, 'finish_node': False})
        
    info = sorted(info, key=lambda x: x['ID'])

    return info




