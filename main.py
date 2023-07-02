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
        self.imagen = PhotoImage(file = "ruta-critica/metroproject.png")
        main_window.background = Label(image = self.imagen, text = "fondo")
        main_window.background.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        main_window.resizable(0,0)
        self.icono = tk.PhotoImage(file="ruta-critica/metroproject - logo.png")
        main_window.iconphoto(True, self.icono)

        self.identificacion = ttk.Entry(
            width= 4,
        )
    
        self.identificacion.place(
            x=142, y=159,
        )

        self.duracion = ttk.Entry(
            width= 4,
        )
    
        self.duracion.place(
            x=335, y=159,
        )

        self.predecesor = ttk.Entry(
            width= 4,
        )
    
        self.predecesor.place(
            x=528, y=159,
        )

        self.descripcion = ttk.Entry(
            width= 35,
        )
    
        self.descripcion.place(
            x=172, y=269,
        )

        self.anadir = tk.Button(
            main_window,
            text = "+",
            font = ("Inter", 20),
            bg = "#e691ca",
            fg = "black",
            command= self.agregar,
            relief="flat",
        )

        self.anadir.place(
            x=476, y=240
        )



        self.ruta = tk.Button(
            main_window,
            text = "Calcular",
            font = ("Inter", 14),
            bg = "#e691ca",
            fg = "black",
            command= self.calcular,
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
        actividad["duracion"] = time
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
        g.runCPM(info)


main_window = tk.Tk()
app = Aplication(main_window)
app.mainloop()