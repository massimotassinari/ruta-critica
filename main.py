import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, Label
import grafo as g
import funciones as f
import networkx as nx
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import funciones as f



class Aplication(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("MetroProject")
        main_window.geometry("700x420")
        self.imagen = PhotoImage(file="ruta-critica/metroproject.png")
        main_window.background = Label(image=self.imagen, text="fondo")
        main_window.background.place(x=0, y=0, relwidth=1, relheight=1)
        main_window.resizable(0, 0)
        self.icono = tk.PhotoImage(file="ruta-critica/metroproject - logo.png")
        main_window.iconphoto(True, self.icono)

        self.identificacion = ttk.Entry(
            width=4,
        )

        self.identificacion.place(
            x=142, y=159,
        )

        self.duracion = ttk.Entry(
            width=4,
        )

        self.duracion.place(
            x=335, y=159,
        )

        self.predecesor = ttk.Entry(
            width=4,
        )

        self.predecesor.place(
            x=528, y=159,
        )

        self.descripcion = ttk.Entry(
            width=35,
        )

        self.descripcion.place(
            x=172, y=269,
        )

        self.anadir = tk.Button(
            main_window,
            text="+",
            font=("Inter", 20),
            bg="#e691ca",
            fg="black",
            command=self.agregar,
            relief="flat",
        )

        self.anadir.place(
            x=476, y=240
        )

        self.ruta = tk.Button(
            main_window,
            text="Calcular",
            font=("Inter", 14),
            bg="#e691ca",
            fg="black",
            command=self.calcular,
            relief="flat",
        )

        self.ruta.place(
            x=308, y=342
        )

    info = []

    def agregar(self):
        actividad = {}
        id = self.identificacion.get()
        time = self.duracion.get()
        p = self.predecesor.get()
        description = self.descripcion.get()

        p = p.split(sep=',')
        id = id.strip()
        time = time.strip()
        description = description.strip()

        actividad["ID"] = id.upper()
        actividad["descripcion"] = description
        actividad["duracion"] = int(time)
        actividad["predecesor"] = p
        actividad["start_node"] = False
        actividad["finish_node"] = False

        self.info.append(actividad)

        self.identificacion.delete(0, tk.END)
        self.duracion.delete(0, tk.END)
        self.predecesor.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)

    def grafo(self):

        info = f.start_finish_nodes(self.info)
        G, critical_path, start_node,finish_node= g.runCPM(info)

        color_map = []
        for node in G.nodes():
            G.nodes[node]['pos_asign'] = False
            if G.nodes[node]['H'] == 0:
                color_map.append(('#6e46c4'))
            else:
                color_map.append(('#e691ca'))

        # Se establece la posicion de los nodos usando las variables posx y posy
        for node in G.nodes():
            if G.nodes[node] == start_node:
                G.nodes[node]['pos_asign'] = True
            acum_y = 0
            for sucesor in list(G.nodes[node]['sucesor']):
                if G.nodes[sucesor]['pos_asign'] == False:
                    G.nodes[sucesor]['posx'] = G.nodes[node]['posx'] + 2
                    G.nodes[sucesor]['posy'] = G.nodes[node]['posy'] - acum_y
                    G.nodes[sucesor]['pos'] = (
                        G.nodes[sucesor]['posx'], G.nodes[sucesor]['posy'])
                    acum_y = acum_y + 0.5
                    G.nodes[sucesor]['pos_asign'] = True

        # obtiene la posicion de los nodos para pasarselo como parametro a la fucion que pinta el grafo "draw_networkx_nodes"
        pos = nx.get_node_attributes(G, 'pos')

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

        # Se hace pasan los parametros que representan el grafo com una ruta critica
        image_file = "ruta-critica/fondografo.png"
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_facecolor('#d4b7ff')
        nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=500)
        nx.draw_networkx_edges(
            G, pos, alpha=0.6, edge_color='black', arrows=True, **options_arrow)
        nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
        plt.xticks(mapeado, dias)
        plt.title('Actividades de la Ruta Crítica (Nodos en Morado)')
        plt.show()


    def calcular(self):
        info = f.start_finish_nodes(self.info)
        G, C, s, p = g.runCPM(info)

        ventana_secundaria = tk.Toplevel()
        ventana_secundaria.configure(background="#e691ca")
        ventana_secundaria.title("MetroProject")
        ventana_secundaria.resizable(False,False)
        ventana_secundaria.config(width=800, height=700)

        # Título del Reporte
        label_act = tk.Label(ventana_secundaria, bg="#e691ca", fg="#292931", text="Reporte", font=("Inter", 18, "bold")).place(x=360, y=10)

        # Etiquetas cuadro del reporte
        label_act = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| Actividad", font=(
            "Inter", 10, "bold")).place(x=20, y=50)
        label_des = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| Descripción", font=("Inter", 10, "bold")).place(x=100, y=50)
        label_pre = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| Predecesor", font=("Inter", 10, "bold")).place(x=220, y=50)
        label_suc = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| Sucesor", font=("Inter", 10, "bold")).place(x=320, y=50)
        label_D = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| D", font=("Inter", 10, "bold")).place(x=420, y=50)
        label_ES = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| ES", font=("Inter", 10, "bold")).place(x=480, y=50)
        label_EF = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| EF", font=("Inter", 10, "bold")).place(x=540, y=50)
        label_LS = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| LS", font=("Inter", 10, "bold")).place(x=600, y=50)
        label_LF = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| LF", font=("Inter", 10, "bold")).place(x=660, y=50)
        label_H = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| H", font=("Inter", 10, "bold")).place(x=720, y=50)
        
        label_H = tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="_____________________________________________________________________________________________________________", font=("Inter", 10, "bold")).place(x=20, y=70)

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
        
            aux_predecesor = str(aux_predecesor)[1:-1]
            aux_sucesor = str(aux_sucesor)[1:-1]

            tk.Label(ventana_secundaria, fg="#292931", bg="#e691ca", text="| " +
                            str(node), font=("Inter", 10)).place(x=20, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['descripcion']), font=("Inter", 7)).place(x=100, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + aux_predecesor,
                            font=("Inter", 10)).place(x=220, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + aux_sucesor,
                            font=("Inter", 10)).place(x=320, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['D']) + " días", font=("Inter", 10)).place(x=420, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['ES']) + " días", font=("Inter", 10)).place(x=480, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['EF']) + " días", font=("Inter", 10)).place(x=540, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca",text="| " + str(
                G.nodes[node]['LS']) + " días", font=("Inter", 10)).place(x=600, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['LF']) + " días", font=("Inter", 10)).place(x=660, y=pos_y)
            tk.Label(ventana_secundaria, fg="#292931",bg="#e691ca", text="| " + str(
                G.nodes[node]['H']) + " días", font=("Inter", 10)).place(x=720, y=pos_y)

        pos_y += 50

        text3 = 'Actividades de la ruta crítica: ' + \
                str(C)[1:-1]
        show_text = text3
        label_CP = tk.Label(ventana_secundaria, fg='#292931',bg="#e691ca", text=show_text, wraplength=600, font=("Inter", 10, "bold")).place(x=20, y=pos_y)

        self.grafo_mostrar = tk.Button(
            ventana_secundaria,
            text="Ver grafo",
            font=("Inter", 14),
            bg="#6e46c4",
            fg="black",
            command=self.grafo,
            relief="flat",
        )

        self.grafo_mostrar.place(
            x=360, y=582
        )


main_window = tk.Tk()
app = Aplication(main_window)
app.mainloop()
