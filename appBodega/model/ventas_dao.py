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

def insertar_venta(cliente_nombre, productos):
    conexion = ConexionDB()  # Instancia de conexión
    
    # Crear un diccionario para almacenar los productos con sus cantidades
    productos_dict = {}
    
    for producto in productos:
        nombre, cantidad = producto.split(" x ")  # Asumiendo que el formato es "Nombre x Cantidad"
        cantidad = float(cantidad.split(" ($")[0])  # Extraer la cantidad del formato "x Cantidad ($Subtotal)"
        subtotal = float(producto.split("($")[1].replace(")", "").replace(",", "").strip())  # Extraer el subtotal
        productos_dict[nombre] = {
            "cantidad": cantidad,
            "subtotal": subtotal
        }

    # Calcular el total basado en los subtotales del diccionario
    total = sum(item["subtotal"] for item in productos_dict.values())
    
    # Convertir el diccionario a una cadena para almacenamiento
    productos_formateados = ", ".join([f"{nombre} x {info['cantidad']}" for nombre, info in productos_dict.items()])
    
    sql = '''
    INSERT INTO ventas (CLIENTE_NOMBRE, PRODUCTOS, TOTAL)
    VALUES (?, ?, ?)
    '''
    conexion.cursor.execute(sql, (cliente_nombre, productos_formateados, total))
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

def modificar_venta(venta_id, nuevo_cliente_nombre, nuevos_productos):
    conexion = ConexionDB()  # Instancia de conexión
    total_nuevo = calcular_total(nuevos_productos)  # Calcula el nuevo total
    
    sql = '''
    UPDATE ventas 
    SET CLIENTE_NOMBRE=?, PRODUCTOS=?, TOTAL=? 
    WHERE ID_VENTA=?
    '''
    
    conexion.cursor.execute(sql, (nuevo_cliente_nombre, nuevos_productos, total_nuevo, venta_id))
    conexion.cerrar()