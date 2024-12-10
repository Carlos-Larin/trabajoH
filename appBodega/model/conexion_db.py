import os
import sqlite3

class ConexionDB:
    def __init__(self):
        self.base_datos = 'database/bodega.db'
        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(self.base_datos), exist_ok=True)
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()