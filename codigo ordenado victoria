import tkinter as tk
from tkinter import messagebox
import sqlite3

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Tiendas")
        self.ventana.geometry("700x400")

        # --- Frames principales ---
        self.frame_formulario = tk.Frame(self.ventana, pady=10)
        self.frame_botones = tk.Frame(self.ventana, pady=10)
        self.frame_lista = tk.Frame(self.ventana, pady=10)

        self.frame_formulario.pack()
        self.frame_botones.pack()
        self.frame_lista.pack(fill=tk.BOTH, expand=True)

        # --- Widgets del formulario ---
        tk.Label(self.frame_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.campo_nombre = tk.Entry(self.frame_formulario, width=40)
        self.campo_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_formulario, text="Horario:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.campo_horario = tk.Entry(self.frame_formulario, width=40)
        self.campo_horario.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_formulario, text="Ubicación:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.campo_ubicacion = tk.Entry(self.frame_formulario, width=40)
        self.campo_ubicacion.grid(row=2, column=1, padx=5, pady=5)

        # --- Botones ---
        self.boton_add = tk.Button(self.frame_botones, text="Añadir Tienda", command=self.añadir_tienda)
        self.boton_add.grid(row=0, column=0, padx=10)

        self.boton_update = tk.Button(self.frame_botones, text="Modificar Tienda", command=self.modificar_tienda)
        self.boton_update.grid(row=0, column=1, padx=10)

        self.boton_delete = tk.Button(self.frame_botones, text="Eliminar Tienda", command=self.eliminar_tienda)
        self.boton_delete.grid(row=0, column=2, padx=10)

    

        # --- Lista de tiendas ---
        tk.Label(self.frame_lista, text="Tiendas Registradas:").pack(anchor="w")
        self.lista_tiendas = tk.Listbox(self.frame_lista, width=60, height=10)
        self.lista_tiendas.pack(fill=tk.BOTH, expand=True)
        self.lista_tiendas.bind("<<ListboxSelect>>", self.cargar_tienda_seleccionada)

        # --- Base de datos ---
        self.conexion = sqlite3.connect("tiendas.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

        # Cargar al iniciar
        self.actualizar_lista()

    # ================================================================
    # BASE DE DATOS
    # ================================================================
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tienda (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            horario TEXT,
            ubicacion TEXT,
            completada INTEGER DEFAULT 0
        )
        """)
        self.conexion.commit()

    # ================================================================
    # MÉTODOS CRUD
    # ================================================================
    def añadir_tienda(self):
        nombre = self.campo_nombre.get().strip()
        horario = self.campo_horario.get().strip()
        ubicacion = self.campo_ubicacion.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
            return

        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion) VALUES (?, ?, ?)",
            (nombre, horario, ubicacion)
        )
        self.conexion.commit()

        self.limpiar_campos()
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_tiendas.delete(0, tk.END)

        self.cursor.execute("SELECT id, nombre, horario, ubicacion, completada FROM Tienda ORDER BY id")
        tiendas = self.cursor.fetchall()

        for t in tiendas:
            id_, nombre, horario, ubicacion, completada = t
            estado = "[X]" if completada else "[ ]"
            texto = f"{id_}: {estado} {nombre} — {horario} — {ubicacion}"
            self.lista_tiendas.insert(tk.END, texto)

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_horario.delete(0, tk.END)
        self.campo_ubicacion.delete(0, tk.END)
        self.lista_tiendas.selection_clear(0, tk.END)

    # ================================================================
    # SELECCIÓN DE LISTA
    # ================================================================
    def get_id_seleccionado(self):
        try:
            seleccionado = self.lista_tiendas.get(self.lista_tiendas.curselection())
            id_tienda = int(seleccionado.split(":")[0])
            return id_tienda
        except:
            return None

    def cargar_tienda_seleccionada(self, event):
        id_tienda = self.get_id_seleccionado()
        if not id_tienda:
            return

        self.cursor.execute(
            "SELECT nombre, horario, ubicacion FROM Tienda WHERE id = ?",
            (id_tienda,)
        )
        tienda = self.cursor.fetchone()

        if tienda:
            nombre, horario, ubicacion = tienda
            self.campo_nombre.delete(0, tk.END)
            self.campo_horario.delete(0, tk.END)
            self.campo_ubicacion.delete(0, tk.END)

            self.campo_nombre.insert(0, nombre)
            self.campo_horario.insert(0, horario)
            self.campo_ubicacion.insert(0, ubicacion)

    # ================================================================
    # MODIFICAR / ELIMINAR / COMPLETAR
    # ================================================================
    def eliminar_tienda(self):
        id_tienda = self.get_id_seleccionado()
        if not id_tienda:
            messagebox.showinfo("Sin selección", "Selecciona una tienda primero.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar esta tienda?"):
            self.cursor.execute("DELETE FROM Tienda WHERE id = ?", (id_tienda,))
            self.conexion.commit()
            self.actualizar_lista()
            self.limpiar_campos()

    def modificar_tienda(self):
        id_tienda = self.get_id_seleccionado()
        if not id_tienda:
            messagebox.showinfo("Sin selección", "Selecciona una tienda primero.")
            return

        nombre = self.campo_nombre.get().strip()
        horario = self.campo_horario.get().strip()
        ubicacion = self.campo_ubicacion.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
            return

        self.cursor.execute(
            "UPDATE Tienda SET nombre=?, horario=?, ubicacion=? WHERE id=?",
            (nombre, horario, ubicacion, id_tienda)
        )
        self.conexion.commit()

        self.actualizar_lista()
        self.limpiar_campos()


# --- Lanzar App ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = App(ventana_principal)
    ventana_principal.mainloop()
