import tkinter as tk
from tkinter import messagebox
import sqlite3

class App:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Tiendas")
        self.ventana.geometry("700x400")

        # ====== Color de fondo general ======
        COLOR_FONDO = "#D7ECFF"   # azul clarito

        self.ventana.configure(bg=COLOR_FONDO)

        # ====== Base de datos ======
        self.conexion = sqlite3.connect("tiendas.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

        # ====== Frames ======
        frame_form = tk.Frame(ventana, pady=10, bg=COLOR_FONDO)
        frame_form.pack()

        frame_bot = tk.Frame(ventana, pady=10, bg=COLOR_FONDO)
        frame_bot.pack()

        frame_lista = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_lista.pack(fill=tk.BOTH, expand=True)

        # ====== Campos ======
        tk.Label(frame_form, text="Nombre:", bg=COLOR_FONDO).pack(anchor="w")
        self.campo_nombre = tk.Entry(frame_form, width=40)
        self.campo_nombre.pack()

        tk.Label(frame_form, text="Horario:", bg=COLOR_FONDO).pack(anchor="w")
        self.campo_horario = tk.Entry(frame_form, width=40)
        self.campo_horario.pack()

        tk.Label(frame_form, text="Ubicación:", bg=COLOR_FONDO).pack(anchor="w")
        self.campo_ubicacion = tk.Entry(frame_form, width=40)
        self.campo_ubicacion.pack()

        tk.Label(frame_form, text="Trabajadores:", bg=COLOR_FONDO).pack(anchor="w")
        self.campo_trab = tk.Entry(frame_form, width=40)
        self.campo_trab.pack()

        # ====== Botones ======
        tk.Button(frame_bot, text="Añadir", command=self.añadir).grid(row=0, column=0, padx=10)
        tk.Button(frame_bot, text="Modificar", command=self.modificar).grid(row=0, column=1, padx=10)
        tk.Button(frame_bot, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=10)

        # ====== Lista ======
        tk.Label(frame_lista, text="Tiendas registradas:", bg=COLOR_FONDO).pack(anchor="w")
        
        self.lista = tk.Listbox(frame_lista, width=70, height=10)
        self.lista.pack(fill=tk.BOTH, expand=True)
        self.lista.bind("<<ListboxSelect>>", self.cargar_seleccion)

        # Cargar lista al iniciar
        self.actualizar_lista()

    # ====================================================
    # BASE DE DATOS
    # ====================================================
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tienda (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                horario TEXT,
                ubicacion TEXT,
                trabajadores TEXT
            )
        """)
        self.conexion.commit()

    # ====================================================
    # FUNCIONES CRUD
    # ====================================================
    def añadir(self):
        nombre = self.campo_nombre.get().strip()
        horario = self.campo_horario.get().strip()
        ubicacion = self.campo_ubicacion.get().strip()
        trab = self.campo_trab.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
            return

        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion, trabajadores) VALUES (?, ?, ?, ?)",
            (nombre, horario, ubicacion, trab)
        )
        self.conexion.commit()

        self.limpiar()
        self.actualizar_lista()

    def modificar(self):
        id_tienda = self.id_seleccionado()
        if not id_tienda:
            messagebox.showinfo("Atención", "Selecciona una tienda.")
            return

        nombre = self.campo_nombre.get()
        horario = self.campo_horario.get()
        ubicacion = self.campo_ubicacion.get()
        trab = self.campo_trab.get()

        self.cursor.execute(
            "UPDATE Tienda SET nombre=?, horario=?, ubicacion=?, trabajadores=? WHERE id=?",
            (nombre, horario, ubicacion, trab, id_tienda)
        )
        self.conexion.commit()

        self.limpiar()
        self.actualizar_lista()

    def eliminar(self):
        id_tienda = self.id_seleccionado()
        if not id_tienda:
            messagebox.showinfo("Atención", "Selecciona una tienda.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar esta tienda?"):
            self.cursor.execute("DELETE FROM Tienda WHERE id=?", (id_tienda,))
            self.conexion.commit()

            self.limpiar()
            self.actualizar_lista()

    # ====================================================
    # LISTA / SELECCIÓN
    # ====================================================
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)

        self.cursor.execute("SELECT * FROM Tienda")
        for id_, nom, hor, ubi, trab in self.cursor.fetchall():
            texto = f"{id_}: {nom} — {hor} — {ubi} — Trabajadores: {trab}"
            self.lista.insert(tk.END, texto)

    def id_seleccionado(self):
        try:
            texto = self.lista.get(self.lista.curselection())
            return int(texto.split(":")[0])
        except:
            return None

    def cargar_seleccion(self, event):
        id_tienda = self.id_seleccionado()
        if not id_tienda:
            return

        self.cursor.execute("SELECT nombre, horario, ubicacion, trabajadores FROM Tienda WHERE id=?", (id_tienda,))
        tienda = self.cursor.fetchone()

        if tienda:
            nombre, horario, ubicacion, trab = tienda
            self.campo_nombre.delete(0, tk.END)
            self.campo_horario.delete(0, tk.END)
            self.campo_ubicacion.delete(0, tk.END)
            self.campo_trab.delete(0, tk.END)

            self.campo_nombre.insert(0, nombre)
            self.campo_horario.insert(0, horario)
            self.campo_ubicacion.insert(0, ubicacion)
            self.campo_trab.insert(0, trab)

    def limpiar(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_horario.delete(0, tk.END)
        self.campo_ubicacion.delete(0, tk.END)
        self.campo_trab.delete(0, tk.END)
        self.lista.selection_clear(0, tk.END)


# Lanzar app
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
