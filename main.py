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
            completada INTEGER DEFAULT 0
        )
        """)
        self.conexion.commit()

    def añadir_tienda(self, nombre, horario, ubicacion):
        self.cursor.execute(
            "INSERT INTO Tienda (nombre, horario, ubicacion) VALUES (?, ?, ?)",
            (nombre, horario, ubicacion)
        )
        self.conexion.commit()

    def actualizar_lista(self, termino=None):
        if termino:
            t = f"%{termino}%"
            self.cursor.execute("""
                SELECT id, nombre, horario, ubicacion, completada
                FROM Tienda
                WHERE nombre LIKE ? OR ubicacion LIKE ? OR horario LIKE ?
                ORDER BY id DESC
            """, (t, t, t))
        else:
            self.cursor.execute("""
                SELECT id, nombre, horario, ubicacion, completada
                FROM Tienda
                ORDER BY id DESC
            """)
        return self.cursor.fetchall()

    def cargar_tienda(self, id_tienda):
        self.cursor.execute("""
            SELECT nombre, horario, ubicacion
            FROM Tienda WHERE id = ?
        """, (id_tienda,))
        return self.cursor.fetchone()

    def modificar_tienda(self, tienda_id, nombre, horario, ubicacion):
        self.cursor.execute("""
            UPDATE Tienda
            SET nombre = ?, horario = ?, ubicacion = ?
            WHERE id = ?
        """, (nombre, horario, ubicacion, tienda_id))
        self.conexion.commit()

    def eliminar_tienda(self, tienda_id):
        self.cursor.execute("DELETE FROM Tienda WHERE id = ?", (tienda_id,))
        self.conexion.commit()

    def marcar_completada(self, tienda_id):
        # Obtener estado actual
        self.cursor.execute("SELECT completada FROM Tienda WHERE id = ?", (tienda_id,))
        estado_actual = self.cursor.fetchone()[0]

        # Alternar
        nuevo_estado = 1 if estado_actual == 0 else 0

        # Guardar
        self.cursor.execute(
            "UPDATE Tienda SET completada = ? WHERE id = ?",
            (nuevo_estado, tienda_id)
        )
        self.conexion.commit()

    def obtener_todas_las_tiendas(self):
        self.cursor.execute("""
            SELECT id, nombre, horario, ubicacion, completada
            FROM Tienda ORDER BY id DESC
        """)
        return self.cursor.fetc
 
  def actualizar_lista(self, termino_busqueda=None):
        if termino_busqueda:
            # Si nos dan un término de búsqueda, filtramos con LIKE
            # Ponemos '%' alrededor del término para buscar en cualquier parte
            termino = f"%{termino_busqueda}%"
            self.cursor.execute("SELECT ... FROM Tarea WHERE descripcion LIKE ?", (termino,))
        else:
            # Si no hay término, seleccionamos todo (como antes)
            self.cursor.execute("SELECT ... FROM Tarea ORDER BY fecha_limite")
            
        tareas = self.cursor.fetchall()
        return tareas

# Este método se llama desde el botón "Buscar"
    def buscar_tareas(self):
        termino = self.campo_busqueda.get()
        self.actualizar_lista_gui(termino) # Llamamos al actualizador con el término

    # Este método se llama desde el botón "Limpiar"
    def limpiar_busqueda(self):
        self.campo_busqueda.delete(0, tk.END)
        self.actualizar_lista_gui() # Llamamos al actualizador sin término

    # Modificamos el actualizador de la GUI para que pase el término
    def actualizar_lista_gui(self, termino_busqueda=None):
        self.lista_tareas.delete(0, tk.END)
        
        # Pedimos los datos (filtrados o no) al gestor de la BD
        tareas = self.db.actualizar_lista(termino_busqueda)
        
        for tarea in tareas:
            # ... (el mismo bucle 'for' que ya teníais) ...
