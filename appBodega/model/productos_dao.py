from .conexion_db import ConexionDB

def crear_tabla():
    conexion = ConexionDB()  # Instancia de conexión
    sql = '''
    CREATE TABLE IF NOT EXISTS productos (
        ITEM VARCHAR(25),
        DESCRIPTION VARCHAR(100),
        QTY DECIMAL(10, 2),
        RATE DECIMAL(10, 2),
        AMOUNT DECIMAL(10, 2)
    )
    '''
    conexion.cursor.execute(sql)
    conexion.cerrar()

def borrar_tabla():
    conexion = ConexionDB()  # Instancia de conexión
    sql = 'DROP TABLE IF EXISTS productos'  # Asegúrate de que la tabla exista antes de borrarla
    conexion.cursor.execute(sql)
    conexion.cerrar()

def insertar_producto(item, description, qty, rate):
    conexion = ConexionDB()  # Instancia de conexión
    sql = '''
    INSERT INTO productos (ITEM, DESCRIPTION, QTY, RATE, AMOUNT)
    VALUES (?, ?, ?, ?, ?)
    '''
    amount = qty * rate  # Calcula el monto total
    conexion.cursor.execute(sql, (item, description, qty, rate, amount))
    conexion.cerrar()

def ver_productos():
    conexion = ConexionDB()  # Instancia de conexión
    sql = 'SELECT * FROM productos'
    
    conexion.cursor.execute(sql)
    registros = conexion.cursor.fetchall()  # Obtiene todos los registros
    
    conexion.cerrar()
    return registros  # Devuelve los registros para su uso posterior

def borrar_producto(item):
    conexion = ConexionDB()  # Instancia de conexión
    sql = 'DELETE FROM productos WHERE ITEM=?'
    conexion.cursor.execute(sql, (item,))
    conexion.cerrar()


def modificar_producto(item_original, nuevo_item, nueva_descripcion, nueva_cantidad, nuevo_precio):
    """Modifica un producto existente en la base de datos."""
    conexion = ConexionDB()  # Instancia de conexión
    nuevo_monto = nueva_cantidad * nuevo_precio  # Calcular el monto total
    sql = '''
    UPDATE productos
    SET ITEM = ?, DESCRIPTION = ?, QTY = ?, RATE = ?, AMOUNT = ?
    WHERE ITEM = ?
    '''
    conexion.cursor.execute(sql, (nuevo_item, nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_monto, item_original))
    conexion.cerrar()

