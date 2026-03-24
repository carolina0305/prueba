import sqlite3

class DatabaseManager:
    def __init__(self, db_path='tiendas.db'):
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tienda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            horario TEXT,
            ubicacion TEXT,
            trabajadores TEXT,
            favoritas TEXT
        )
        """)
        self.conexion.commit()

    def añadir_tienda(self, nombre, horario, ubicacion, trabajadores, favoritas):
        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion, trabajadores, favoritas) VALUES (?, ?, ?, ?, ?)",
            (nombre, horario, ubicacion, trabajadores, favoritas)
        )
        self.conexion.commit()

    def obtener_todas_las_tiendas(self):
        self.cursor.execute("SELECT * FROM Tienda ORDER BY id DESC")
        return self.cursor.fetchall()

    def cargar_tienda(self, id_tienda):
        self.cursor.execute("SELECT nombre, horario, ubicacion, trabajadores, favoritas FROM Tienda WHERE id = ?", (id_tienda,))
        return self.cursor.fetchone()

    def modificar_tienda(self, tienda_id, nombre, horario, ubicacion, trabajadores, favoritas):
        self.cursor.execute("""
            UPDATE Tienda
            SET nombre = ?, horario = ?, ubicacion = ?, trabajadores = ?, favoritas = ?
            WHERE id = ?
        """, (nombre, horario, ubicacion, trabajadores, favoritas, tienda_id))
        self.conexion.commit()

    def eliminar_tienda(self, tienda_id):
        self.cursor.execute("DELETE FROM Tienda WHERE id = ?", (tienda_id,))
        self.conexion.commit()
