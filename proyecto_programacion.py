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

# --- Botones ---
boton_add = tk.Button(ventana, text="Añadir tienda favorita")
boton_update = tk.Button(ventana, text="Modificar tienda favorita")
boton_delete = tk.Button(ventana, text="Eliminar tienda favorita")

# --- Lista de Tareas ---
etiqueta_lista = tk.Label(ventana, text="Productos")
lista_productos = tk.Listbox(ventana, width=60, height=10)

# 3. Posicionamiento con Grid
# --- Formulario de Entrada ---
etiqueta_hora.grid(row=0, column=0, padx=10, pady=5, sticky="w")
campo_hora.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="ew")

etiqueta_nomb.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_nomb.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

etiqueta_ubic.grid(row=1, column=2, padx=10, pady=5, sticky="w")
campo_ubic.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

# --- Botones ---
boton_add.grid(row=2, column=1, padx=10, pady=10)
boton_update.grid(row=2, column=2, padx=10, pady=10)
boton_delete.grid(row=2, column=3, padx=10, pady=10)

# --- Lista de Tareas ---
etiqueta_lista.grid(row=3, column=0, padx=10, pady=5, sticky="w")
lista_productos.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")


# 4. Iniciar el bucle de la aplicación
ventana.mainloop()


import tkinter as tk  # Importamos la librería

ventana = tk.Tk()  # Creamos la ventana principal
ventana.title("ventana2.py")  # Le ponemos un título

# Creamos una etiqueta
etiqueta_nombre = tk.Label(ventana, text="Nombre:ventana2.py")

# La colocamos en la fila 0, columna 0
etiqueta_nombre.grid(row=0, column=0)

ventana.mainloop()  # Mantiene la ventana abierta y a la espera de acciones º
