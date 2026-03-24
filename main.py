import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import json


class App:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Tiendas")
        self.ventana.geometry("700x450")

        # Colores
        COLOR_FONDO = "#D7ECFF"
        COLOR_BOTONES = "#F5A4D1"
        COLOR_CAMPOS = "#D7ECFF"
        COLOR_CASILLAS = "#F5A4D1"

        self.ventana.configure(bg=COLOR_FONDO)

        # Base de datos
        self.conexion = sqlite3.connect("tiendas.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

        # MENÚ
        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Exportar a JSON", command=self.exportar_json)
        menu_archivo.add_command(label="Importar desde JSON", command=self.importar_json)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)

        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca_de)

        # FRAMES
        frame_form = tk.Frame(self.ventana, pady=10, bg=COLOR_FONDO)
        frame_form.pack()

        frame_bot = tk.Frame(self.ventana, pady=10, bg=COLOR_FONDO)
        frame_bot.pack()

        frame_lista = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_lista.pack(fill=tk.BOTH, expand=True)

        # CAMPOS
        tk.Label(frame_form, text="Nombre:", bg=COLOR_CAMPOS).pack(anchor="w")
        self.campo_nombre = tk.Entry(frame_form, width=40, bg=COLOR_CASILLAS)
        self.campo_nombre.pack()

        tk.Label(frame_form, text="Horario:", bg=COLOR_CAMPOS).pack(anchor="w")
        self.campo_horario = tk.Entry(frame_form, width=40, bg=COLOR_CASILLAS)
        self.campo_horario.pack()

        tk.Label(frame_form, text="Ubicación:", bg=COLOR_CAMPOS).pack(anchor="w")
        self.campo_ubicacion = tk.Entry(frame_form, width=40, bg=COLOR_CASILLAS)
        self.campo_ubicacion.pack()

        tk.Label(frame_form, text="Trabajadores:", bg=COLOR_CAMPOS).pack(anchor="w")
        self.campo_trab = tk.Entry(frame_form, width=40, bg=COLOR_CASILLAS)
        self.campo_trab.pack()

        tk.Label(frame_form, text="Prioridad:", bg=COLOR_CAMPOS).pack(anchor="w")
        self.combo_prio = ttk.Combobox(frame_form, values=["Baja", "Media", "Alta"], state="readonly")
        self.combo_prio.pack(fill=tk.X)
        self.combo_prio.current(1)

        # BOTONES
        tk.Button(frame_bot, text="Añadir", command=self.añadir, bg=COLOR_BOTONES).grid(row=0, column=0, padx=10)
        tk.Button(frame_bot, text="Modificar", command=self.modificar, bg=COLOR_BOTONES).grid(row=0, column=1, padx=10)
        tk.Button(frame_bot, text="Eliminar", command=self.eliminar, bg=COLOR_BOTONES).grid(row=0, column=2, padx=10)

        # LISTA
        tk.Label(frame_lista, text="Tiendas registradas:", bg=COLOR_FONDO).pack(anchor="w")
        self.lista = tk.Listbox(frame_lista, width=70, height=10)
        self.lista.pack(fill=tk.BOTH, expand=True)
        self.lista.bind("<<ListboxSelect>>", self.cargar_seleccion)

        self.actualizar_lista()

    # ========================
    # JSON
    # ========================
    def exportar_json(self):
        self.cursor.execute("SELECT * FROM Tienda")
        tiendas = self.cursor.fetchall()

        lista = []
        for t in tiendas:
            datos = list(t) + [""] * (6 - len(t))
            lista.append({
                "id": datos[0],
                "nombre": datos[1],
                "horario": datos[2],
                "ubicacion": datos[3],
                "trabajadores": datos[4],
                "prioridad": datos[5]
            })

        try:
            with open("backup_tiendas.json", "w", encoding="utf-8") as f:
                json.dump(lista, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", "Exportado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def importar_json(self):
        try:
            with open("backup_tiendas.json", "r", encoding="utf-8") as f:
                datos = json.load(f)

            for t in datos:
                self.cursor.execute(
                    "INSERT INTO Tienda (nombre, horario, ubicacion, trabajadores, prioridad) VALUES (?, ?, ?, ?, ?)",
                    (
                        t.get("nombre", ""),
                        t.get("horario", ""),
                        t.get("ubicacion", ""),
                        t.get("trabajadores", ""),
                        t.get("prioridad", "Media")
                    )
                )

            self.conexion.commit()
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Importado correctamente")

        except FileNotFoundError:
            messagebox.showerror("Error", "No existe el archivo JSON")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========================
    # BASE DE DATOS
    # ========================
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tienda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                horario TEXT,
                ubicacion TEXT,
                trabajadores TEXT,
                prioridad TEXT
            )
        """)
        self.conexion.commit()

    # ========================
    # CRUD
    # ========================
    def añadir(self):
        nombre = self.campo_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Nombre vacío")
            return

        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion, trabajadores, prioridad) VALUES (?, ?, ?, ?, ?)",
            (nombre, self.campo_horario.get(), self.campo_ubicacion.get(), self.campo_trab.get(), self.combo_prio.get())
        )
        self.conexion.commit()
        self.limpiar()
        self.actualizar_lista()

    def modificar(self):
        id_ = self.id_seleccionado()
        if not id_:
            return

        self.cursor.execute(
            "UPDATE Tienda SET nombre=?, horario=?, ubicacion=?, trabajadores=?, prioridad=? WHERE id=?",
            (self.campo_nombre.get(), self.campo_horario.get(), self.campo_ubicacion.get(),
             self.campo_trab.get(), self.combo_prio.get(), id_)
        )
        self.conexion.commit()
        self.limpiar()
        self.actualizar_lista()

    def eliminar(self):
        id_ = self.id_seleccionado()
        if not id_:
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            self.cursor.execute("DELETE FROM Tienda WHERE id=?", (id_,))
            self.conexion.commit()
            self.limpiar()
            self.actualizar_lista()

    # ========================
    # LISTA
    # ========================
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM Tienda")

        for t in self.cursor.fetchall():
            datos = list(t) + [""] * (6 - len(t))
            self.lista.insert(tk.END, f"{datos[0]}: {datos[1]} - {datos[2]} - {datos[3]} - {datos[4]} - {datos[5]}")

    def id_seleccionado(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            return None
        texto = self.lista.get(seleccion[0])
        return int(texto.split(":")[0])

    def cargar_seleccion(self, event):
        seleccion = self.lista.curselection()
        if not seleccion:
            return

        id_ = int(self.lista.get(seleccion[0]).split(":")[0])

        self.cursor.execute("SELECT * FROM Tienda WHERE id=?", (id_,))
        t = self.cursor.fetchone()

        if not t:
            return

        datos = list(t) + [""] * (6 - len(t))

        self.campo_nombre.delete(0, tk.END)
        self.campo_horario.delete(0, tk.END)
        self.campo_ubicacion.delete(0, tk.END)
        self.campo_trab.delete(0, tk.END)

        self.campo_nombre.insert(0, datos[1])
        self.campo_horario.insert(0, datos[2])
        self.campo_ubicacion.insert(0, datos[3])
        self.campo_trab.insert(0, datos[4])
        self.combo_prio.set(datos[5])

    def limpiar(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_horario.delete(0, tk.END)
        self.campo_ubicacion.delete(0, tk.END)
        self.campo_trab.delete(0, tk.END)
        self.combo_prio.current(1)
        self.lista.selection_clear(0, tk.END)

    # ========================
    # ACERCA DE
    # ========================
    def mostrar_acerca_de(self):
        top = tk.Toplevel(self.ventana)
        top.title("Acerca de")
        tk.Label(top, text="Gestor de Tiendas v1.0").pack(pady=10)
        tk.Button(top, text="Cerrar", command=top.destroy).pack()


# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
