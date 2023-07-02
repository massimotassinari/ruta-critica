import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, Label
import grafo as g
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

        print(self.info)


    def calcular(self):
        info = f.start_finish_nodes(self.info)
        print(info)
        G, C = g.runCPM(info)

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

        text3 = 'Actividades de la ruta crítica ' + \
                str(C)
        show_text = text3
        label_CP = tk.Label(ventana_secundaria, fg='#292931',bg="#e691ca", text=show_text, wraplength=600, font=("Inter", 10, "bold")).place(x=20, y=pos_y)

main_window = tk.Tk()
app = Aplication(main_window)
app.mainloop()
