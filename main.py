import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk 
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

        # Menu
        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)

        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca_de)

        menu_archivo.add_command(label="Exportar a JSON", command=self.exportar_json)  # 1.3
        menu_archivo.add_command(label="Importar desde JSON", command=self.importar_json)
        menu_archivo.add_separator() # Una línea separadora
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)


        # Esta es la función que hemos conectado al menú
    def exportar_json(self):
        # 1. Pedimos todos los datos al gestor de la BD
        tiendas = self.db.obtener_todas_las_tiendas() # Asumimos que este método existe
        
        lista_de_diccionarios = []
        for tienda in tiendas:
            # Convertimos cada tupla (ej: (1, 'Comprar', ...)) en un diccionario
            diccionario_tienda = {
                'id': tienda[0],
                'Nombre': tienda[1],
                'Trabajadores': tienda[2],
                'Horario': tienda[3],
                'Ubicación': tienda[4]
            }
            lista_de_diccionarios.append(diccionario_tienda)

            # Base de datos
            self.conexion = sqlite3.connect("tiendas.db")
            self.cursor = self.conexion.cursor()
            self.crear_tabla()

            # Frames
            frame_form = tk.Frame(ventana, pady=10, bg=COLOR_FONDO)
            frame_form.pack()

            frame_bot = tk.Frame(ventana, pady=10, bg=COLOR_FONDO)
            frame_bot.pack()

            # Busqueda
            frame_busqueda = tk.Frame(self.ventana)
            frame_busqueda.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
            self.campo_busqueda = tk.Entry(frame_busqueda)
            self.campo_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.boton_buscar = tk.Button(frame_busqueda, text="Buscar", command=self.buscar_tareas)
            self.boton_buscar.pack(side=tk.LEFT, padx=5)

            self.boton_limpiar_busqueda = tk.Button(frame_busqueda, text="Limpiar", command=self.limpiar_busqueda)
            self.boton_limpiar_busqueda.pack(side=tk.LEFT, padx=5)

            frame_lista = tk.Frame(ventana, bg=COLOR_FONDO)
            frame_lista.pack(fill=tk.BOTH, expand=True)

            # Campos
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

            # Bombox
            tk.Label(frame_form, text="Prioridad:", bg=COLOR_CAMPOS).pack(anchor="w")
            self.combo_prio = ttk.Combobox(
                frame_form,
                values=["Baja", "Media", "Alta"],
                state="readonly"  # Para que no se pueda escribir, solo seleccionar
            )
            self.combo_prio.pack(fill=tk.X)
            self.combo_prio.current(1)  # Selecciona "Media" por defecto
            

            # Botones
            tk.Button(frame_bot, text="Añadir", command=self.añadir, bg=COLOR_BOTONES).grid(row=0, column=0, padx=10)
            tk.Button(frame_bot, text="Modificar", command=self.modificar, bg=COLOR_BOTONES).grid(row=0, column=1, padx=10)
            tk.Button(frame_bot, text="Eliminar", command=self.eliminar, bg=COLOR_BOTONES).grid(row=0, column=2, padx=10)

            # Lista
            tk.Label(frame_lista, text="Tiendas registradas:", bg=COLOR_FONDO).pack(anchor="w")
            self.lista = tk.Listbox(frame_lista, width=70, height=10)
            self.lista.pack(fill=tk.BOTH, expand=True)
            self.lista.bind("<<ListboxSelect>>", self.cargar_seleccion)

            # Cargar lista al iniciar
            self.actualizar_lista()

                      
        # 2. Escribimos la lista de diccionarios en un archivo .json
        try:
            with open('backup_tiendas.json', 'w', encoding='utf-8') as f:
                json.dump(lista_de_diccionarios, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportación Exitosa", "Datos exportados a backup_tiendas.json")
        except Exception as e: # Capturamos cualquier error que pueda ocurrir
            messagebox.showerror("Error de Exportación", f"No se pudo exportar: {e}")

     def importar_json(self):
        try:
            with open('backup_tareas.json', 'r', encoding='utf-8') as f:
                # json.load lee el archivo 'f' y lo convierte a una lista de Python
                lista_de_tareas = json.load(f)
                
            for tarea in lista_de_tareas:
                # Insertamos cada tarea en la BD usando las claves del diccionario
                self.db.añadir_tarea(
                    tarea['descripcion'],
                    tarea['fecha_limite'],
                    tarea['prioridad']
                )
                # (Nota: esto no importa el estado 'completada' o el 'id', se podría mejorar)
                
            self.actualizar_lista_gui()
            messagebox.showinfo("Importación Exitosa", "Datos importados desde backup_tareas.json")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'backup_tareas.json'")
        except Exception as e:
            messagebox.showerror("Error de Importación", f"No se pudo importar: {e}")

       # Fin 1.3
    # Base
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tienda (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                horario TEXT,
                ubicacion TEXT,
                trabajadores TEXT,
                prioridad TEXT DEFAULT 'Media'  # <-- NUEVO CAMPO
            )
        """)
        self.conexion.commit()

    # Crud
    def añadir(self):
        nombre = self.campo_nombre.get().strip()
        horario = self.campo_horario.get().strip()
        ubicacion = self.campo_ubicacion.get().strip()
        trab = self.campo_trab.get().strip()
        prio = self.combo_prio.get()  # Comboxz

        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
            return

        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion, trabajadores, prioridad) VALUES (?, ?, ?, ?, ?)",
            (nombre, horario, ubicacion, trab, prio) 
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
        prio = self.combo_prio.get()  # Combox

        self.cursor.execute(
            "UPDATE Tienda SET nombre=?, horario=?, ubicacion=?, trabajadores=?, prioridad=? WHERE id=?",
            (nombre, horario, ubicacion, trab, prio, id_tienda)
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

    # Lista
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM Tienda")
        for id_, nom, hor, ubi, trab, prio in self.cursor.fetchall():  # <-- ahora también prio
            texto = f"{id_}: {nom} — {hor} — {ubi} — Trabajadores: {trab} — Prioridad: {prio}"
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

        self.cursor.execute(
            "SELECT nombre, horario, ubicacion, trabajadores, prioridad FROM Tienda WHERE id=?",
            (id_tienda,)
        )
        tienda = self.cursor.fetchone()
        if tienda:
            nombre, horario, ubicacion, trab, prio = tienda
            self.campo_nombre.delete(0, tk.END)
            self.campo_horario.delete(0, tk.END)
            self.campo_ubicacion.delete(0, tk.END)
            self.campo_trab.delete(0, tk.END)

            self.campo_nombre.insert(0, nombre)
            self.campo_horario.insert(0, horario)
            self.campo_ubicacion.insert(0, ubicacion)
            self.campo_trab.insert(0, trab)
            self.combo_prio.set(prio)  # Por combox

    def limpiar(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_horario.delete(0, tk.END)
        self.campo_ubicacion.delete(0, tk.END)
        self.campo_trab.delete(0, tk.END)
        self.combo_prio.current(1)  # El cambio de combo
        self.lista.selection_clear(0, tk.END)

    # Acerca de
    def mostrar_acerca_de(self):
        ventana_acerca_de = tk.Toplevel(self.ventana)
        ventana_acerca_de.title("Acerca de las tiendas")
        ventana_acerca_de.geometry("300x200")
        ventana_acerca_de.grab_set()
        ventana_acerca_de.transient(self.ventana)

        tk.Label(ventana_acerca_de, text="Gestor de Tareas v1.0").pack(pady=20)
        tk.Label(ventana_acerca_de, text="Desarrollado por: [Avril, Carolina y Victoria]").pack(pady=5)
        tk.Button(ventana_acerca_de, text="Cerrar", command=ventana_acerca_de.destroy).pack(pady=20)


# Lanzar app
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
