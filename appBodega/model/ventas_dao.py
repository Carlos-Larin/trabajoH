from .conexion_db import ConexionDB

def crear_tabla_ventas():
    conexion = ConexionDB()  # Instancia de conexión
    sql = '''
    CREATE TABLE IF NOT EXISTS ventas (
        ID_VENTA INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_NOMBRE VARCHAR(100),
        PRODUCTOS TEXT,
        TOTAL DECIMAL(10, 2),
        FECHA TEXT DEFAULT CURRENT_TIMESTAMP
    )
    '''
    conexion.cursor.execute(sql)
    conexion.cerrar()

def insertar_venta(cliente_nombre, productos, total):
    conexion = ConexionDB()

    sql = '''
    INSERT INTO ventas (CLIENTE_NOMBRE, PRODUCTOS, TOTAL)
    VALUES (?, ?, ?)
    '''
    conexion.cursor.execute(sql, (cliente_nombre, productos, total))
    conexion.cerrar()





def calcular_total(productos):
    total = 0.0
    for producto_info in productos.split(','):
        try:
            nombre_producto, cantidad_str = producto_info.split('x')
            cantidad = int(cantidad_str.strip())
            precio_unitario = obtener_precio_unitario(nombre_producto.strip())  # Implementa esta función
            total += cantidad * precio_unitario
        except ValueError:
            continue
    return total

def obtener_precio_unitario(nombre_producto):
    """Obtiene el precio unitario del producto desde la base de datos."""
    conexion = ConexionDB()  # Instancia de conexión
    sql = "SELECT PRECIO FROM productos WHERE NOMBRE=?"
    
    conexion.cursor.execute(sql, (nombre_producto,))
    resultado = conexion.cursor.fetchone()
    
    conexion.cerrar()
    
    return resultado[0] if resultado else 0.0  # Devuelve el precio o 0 si no se encuentra

def ver_ventas():
    conexion = ConexionDB()  # Instancia de conexión
    sql = 'SELECT * FROM ventas'
    
    conexion.cursor.execute(sql)
    registros = conexion.cursor.fetchall()  # Obtiene todos los registros
    
    conexion.cerrar()
    return registros  # Devuelve los registros para su uso posterior

def borrar_venta(venta_id):
    conexion = ConexionDB()  # Instancia de conexión
    sql = 'DELETE FROM ventas WHERE ID_VENTA=?'
    conexion.cursor.execute(sql, (venta_id,))
    conexion.cerrar()

