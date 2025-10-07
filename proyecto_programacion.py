
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





