class Tienda:

    def __init__(self,ubicacion,trabajadores,nombre,horario=False):

        self.id = None
        self.ubicacion = ubicacion
        self.trabajadores = trabajadores
        self.nombre = nombre 
        self.horario = horario



# --- CODIGO DE PRUEVA ---

tienda1 = Tienda("Hacer una lista de las tiendas que abre pronto abre a la que menos" , "2025-10-20" , "Alta")
tienda2 = Tienda("Hacer una lista de tiendas en orden alfabetico" , "2025-18-10" , "Media")

print("--- DATOS DE LA TAREA 1 ---")
print("Hacer una lista de las tiendas que abre pronto abre a la que menos")
print(f"ubicacaion: {tienda1.ubicacion}")
print(f"trabajadores: {tienda1.trabajadores}")
print(f"nombre: {tienda1.nombre}")
print(f"horario: {tienda1.horario}")

print("\n--- DATOS DE LA TAREA 2 ---") # '\\n' añade una línea en blanco para separar
print(f"Hacer una lista de tiendas en orden alfabetico")
print(f"ubicacaion: {tienda2.ubicacion}")
print(f"trabajadores: {tienda2.trabajadores}")
print(f"nombre: {tienda2.nombre}")
print(f"horario: {tienda2.horario}")

import tkinter as tk
import sqlite3

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Tareas")
        # ... aquí irá todo el código de la interfaz ...

        # 1. Ventana principal
        ventana = tk.Tk()
        ventana.title("Listado de tiendas")
        ventana.geometry("700x400")  # Ancho x Alto


        # 2. Creación de Widgets
        # --- Formulario de Entrada ---
        etiqueta_hora = tk.Label(ventana, text="Horario")
        campo_hora = tk.Entry(ventana, width=40)

        etiqueta_nomb = tk.Label(ventana, text="Nombre:")
        campo_nomb = tk.Entry(ventana)

        etiqueta_ubic = tk.Label(ventana, text="Ubicación")
        campo_ubic = tk.Entry(ventana)

        etiqueta_trab = tk.Label(ventana, text="Trabajadores:")
        campo_trab = tk.Entry(ventana)

        # Botón de Avril

        def insertar():
            print("Insertando tienda a la lista")

        # Botón 

        def modificar():
            print("Modificar tienda favorita")

        # Botón 

        def eliminar():
            print("Eliminar tienda favorita")        


        # --- Botones ---
        boton_add = tk.Button(ventana, text="Añadir tienda favorita", command=insertar)
        boton_update = tk.Button(ventana, text="Modificar tienda favorita", command=modificar)
        boton_delete = tk.Button(ventana, text="Eliminar tienda favorita", command=eliminar)

        # --- Lista de Tareas ---
        etiqueta_lista = tk.Label(ventana, text="Tiendas")
        lista_productos = tk.Listbox(ventana, width=60, height=10)

        # 3. Posicionamiento con Grid
        # --- Formulario de Entrada ---
        etiqueta_hora.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        campo_hora.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="ew")

        etiqueta_nomb.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        campo_nomb.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        etiqueta_ubic.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        campo_ubic.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        etiqueta_trab.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        campo_trab.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # --- Botones ---
        boton_add.grid(row=2, column=1, padx=10, pady=10)
        boton_update.grid(row=2, column=2, padx=10, pady=10)
        boton_delete.grid(row=2, column=3, padx=10, pady=10)

        # --- Lista de Tareas ---
        etiqueta_lista.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        lista_productos.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")


        # 4. Iniciar el bucle de la aplicación
        ventana.mainloop()


        # --- PASO 1: Conectar a la base de datos ---
        # Se crea el archivo 'tareas.db' si no existe
        conexion = sqlite3.connect('tareas.db')

        # Para poder enviar comandos, necesitamos un "cursor"
        cursor = conexion.cursor()

        # --- PASO 2: Ejecutar un comando SQL ---
        # Usamos un string multilínea con triples comillas para que el SQL sea más legible
        comando_sql = """
        CREATE TABLE IF NOT EXISTS Tienda (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            horario INTEGER,
            ubicación TEXT,
            trabajadores INTEGER
        )
        """




        # 'IF NOT EXISTS' evita que nos dé un error si la tabla ya ha sido creada
        cursor.execute(comando_sql)

        # Para que los cambios se guarden de forma permanente, hacemos un "commit"
        conexion.commit()

        # --- PASO 3: Cerrar la conexión ---
        conexion.close()

        print("Tabla 'Tarea' creada con éxito (si no existía ya).")



# --- Código para lanzar la aplicación ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = App(ventana_principal)
    ventana_principal.mainloop()




# Dentro de __init__ en la clase App

# --- Creación de Frames para organizar ---
frame_formulario = tk.Frame(self.ventana, pady=10)
frame_botones = tk.Frame(self.ventana)
frame_lista = tk.Frame(self.ventana, pady=10)

# --- Posicionamiento de los Frames principales con pack() ---
frame_formulario.pack() # Se apila arriba
frame_botones.pack()    # Se apila debajo del anterior
# El frame de la lista se expandirá para rellenar el resto de la ventana
frame_lista.pack(fill=tk.BOTH, expand=True) 

# AHORA, al crear los widgets, los asignamos a su frame correspondiente
self.etiqueta_desc = tk.Label(frame_formulario, text="Descripción:")

# Y usamos .grid() para posicionarlos DENTRO de ese frame
self.etiqueta_desc.grid(row=0, column=0, padx=5, pady=5, sticky="w")

