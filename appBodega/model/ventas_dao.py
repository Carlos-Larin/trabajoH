from .conexion_db import ConexionDB
from datetime import datetime

def crear_tabla_ventas():
    conexion = ConexionDB()
    sql = '''
    CREATE TABLE IF NOT EXISTS ventas(
       ID_VENTA INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_NOMBRE VARCHAR(100),
        DIRECCION TEXT,
        PRODUCTOS TEXT,
        TOTAL DECIMAL(10, 2),
        FECHA TEXT DEFAULT CURRENT_TIMESTAMP
    )
    '''
    conexion.cursor.execute(sql)
    conexion.cerrar()

def insertar_venta(cliente, direccion, productos, total):
    conexion = ConexionDB()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO ventas (CLIENTE_NOMBRE, DIRECCION, PRODUCTOS, TOTAL, FECHA) VALUES (?, ?, ?, ?, ?)"
    conexion.cursor.execute(sql, (cliente, direccion, productos, total, fecha))
    conexion.cerrar()

def ver_ventas():
    conexion = ConexionDB()
    sql = 'SELECT * FROM ventas'
    conexion.cursor.execute(sql)
    ventas = conexion.cursor.fetchall()
    conexion.cerrar()
    return ventas

def borrar_venta(id_venta):
    conexion = ConexionDB()
    sql = 'DELETE FROM ventas WHERE id_venta = ?'
    conexion.cursor.execute(sql, (id_venta,))
    conexion.cerrar()

