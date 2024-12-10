import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importar ttk para usar Treeview
from model.productos_dao import crear_tabla, insertar_producto, ver_productos, borrar_producto
from model.ventas_dao import crear_tabla_ventas, insertar_venta  # Asegúrate de tener estas funciones

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RJL BDProductos")
        self.root.geometry("800x600")
        self.root.iconbitmap("appBodega/image/bodeg.ico")

        # Crear tablas si no existen al iniciar la aplicación
        crear_tabla()
        crear_tabla_ventas()

        self.frame = tk.Frame(root, bg="peach puff")
        self.frame.pack(pady=20)

        # Definición de campos
        tk.Label(self.frame, text="Nombre del Cliente:", bg="peach puff").grid(row=0, column=0, padx=10, pady=10)
        self.entry_cliente = tk.Entry(self.frame)
        self.entry_cliente.grid(row=0, column=1)

        tk.Label(self.frame, text="ID Producto:", bg="peach puff").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.frame)
        self.entry_id.grid(row=1, column=1)

        tk.Label(self.frame, text="Nombre del Producto:", bg="peach puff").grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=2, column=1)

        tk.Label(self.frame, text="Cantidad:", bg="peach puff").grid(row=3, column=0, padx=10, pady=10)
        self.entry_cantidad = tk.Entry(self.frame)
        self.entry_cantidad.grid(row=3, column=1)

        tk.Label(self.frame, text="Precio por Unidad:", bg="peach puff").grid(row=4, column=0, padx=10, pady=10)
        self.entry_precio_unitario = tk.Entry(self.frame)
        self.entry_precio_unitario.grid(row=4, column=1)

        tk.Label(self.frame, text="Total del Producto:", bg="peach puff").grid(row=5, column=0, padx=10, pady=10)
        self.entry_total_producto = tk.Entry(self.frame)
        self.entry_total_producto.grid(row=5, column=1)

        # Frame para los botones
        button_frame = tk.Frame(root, bg="peach puff")
        button_frame.pack(pady=(10, 20))

        btn_calcular = tk.Button(button_frame, text="Calcular Total", command=self.calcular_total)
        btn_calcular.grid(row=0, column=0, padx=(5, 10))

        btn_guardar = tk.Button(button_frame, text="Guardar Producto", command=self.guardar_producto)
        btn_guardar.grid(row=0, column=1)

        btn_ver_productos = tk.Button(button_frame, text="Ver Productos", command=self.mostrar_productos)
        btn_ver_productos.grid(row=0,column=2)

        btn_borrar = tk.Button(button_frame,text="Borrar Producto",command=self.borrar_producto)
        btn_borrar.grid(row=0,column=3)

        btn_agregar_venta = tk.Button(button_frame,text="Agregar a Venta",command=self.agregar_a_venta)
        btn_agregar_venta.grid(row=0,column=4)

         # Configuración de Treeview para mostrar productos
        self.tree = ttk.Treeview(root)
        
       # Definir columnas en el Treeview
        self.tree["columns"] = ("ID", "Nombre", "Cantidad", "Precio", "Total")
        
        for col in self.tree["columns"]:
                self.tree.heading(col,text=col)  # Encabezados de columnas
                
        self.tree["show"] = "headings"  # Mostrar encabezados
        self.tree.pack(pady=(10 , 20), fill=tk.BOTH)  # Llenar el espacio disponible

    def calcular_total(self):
       """Calcula el total del producto solicitado."""
       try:
           cantidad = int(self.entry_cantidad.get())
           precio_unitario = float(self.entry_precio_unitario.get())
           total_producto = cantidad * precio_unitario
           self.entry_total_producto.delete(0 ,tk.END)  # Limpia el campo antes de insertar
           self.entry_total_producto.insert(0 ,f"{total_producto:.2f}")  # Muestra el total formateado
       except ValueError:
           messagebox.showerror("Error" ,"Por favor ingresa valores válidos.")

    def guardar_producto(self):
       """Guarda los datos del producto en la base de datos."""
       try:
           item = self.entry_id.get()
           nombre_producto = self.entry_nombre.get()
           cantidad = float(self.entry_cantidad.get())
           precio_unitario = float(self.entry_precio_unitario.get())
           
            # Inserta el producto en la base de datos
           insertar_producto(item.strip() ,nombre_producto.strip() ,cantidad ,precio_unitario)  

           messagebox.showinfo("Éxito" ,f"Producto guardado:\nID: {item}\nNombre: {nombre_producto}\nCantidad: {cantidad}\nPrecio Unitario: {precio_unitario}")
           
            # Limpiar campos después de guardar
           self.clear_entries()

            # Actualiza la visualización de productos
           self.mostrar_productos()

       except ValueError:
           messagebox.showerror("Error" ,"Por favor ingresa valores válidos.")

    def mostrar_productos(self):
       """Muestra los productos almacenados en el Treeview."""
       for row in self.tree.get_children():
           self.tree.delete(row)  # Limpia el Treeview antes de mostrar nuevos datos

       productos = ver_productos()  # Llama a la función para obtener productos
        
       for p in productos:
           # Inserta cada producto en el Treeview
           self.tree.insert("" ,"end" ,values=(p[0] ,p[1] ,p[2] ,p[3] ,p[4]))

    def borrar_producto(self):
       """Borra el producto seleccionado del Treeview y de la base de datos."""
       selected_item = self.tree.selection()
       
       if not selected_item:
           messagebox.showwarning("Advertencia" ,"Seleccione un producto para borrar.")
           return
        
       item_id = self.tree.item(selected_item)["values"][0]  # Obtiene el ID del producto seleccionado
        
       borrar_producto(item_id)  # Llama a la función para borrar el producto en la base de datos
        
       messagebox.showinfo("Éxito" ,f"Producto con ID {item_id} ha sido borrado.")
        
       # Actualiza la visualización de productos
       self.mostrar_productos()

    def agregar_a_venta(self):
         """Agrega los productos seleccionados a una venta."""
         cliente_nombre = self.entry_cliente.get().strip()
         if not cliente_nombre:
             messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del cliente.")
             return

         selected_items = [self.tree.item(item)["values"] for item in self.tree.selection()]
         
         if not selected_items:
             messagebox.showwarning("Advertencia", "Seleccione al menos un producto para agregar a la venta.")
             return

         productos_str = ", ".join([f"{item[1]} (Cantidad: {item[2]})" for item in selected_items])
         
         insertar_venta(cliente_nombre ,productos_str)  # Inserta los productos como un solo registro.
         
         for item in selected_items:
             item_id = item[0]
             borrar_producto(item_id)  # Borra el producto después de agregarlo a la venta.

         messagebox.showinfo("Éxito", f"Productos agregados a la venta para {cliente_nombre}.")
         
         # Actualiza la visualización de productos
         self.mostrar_productos()

    def clear_entries(self):
         """Limpia todos los campos de entrada."""
         self.entry_cliente.delete(0 ,tk.END)  # Limpiar campo cliente
         self.entry_id.delete(0 ,tk.END)
         self.entry_nombre.delete(0 ,tk.END)
         self.entry_cantidad.delete(0 ,tk.END)
         self.entry_precio_unitario.delete(0 ,tk.END)
         self.entry_total_producto.delete(0 ,tk.END)

def main():
    root = tk.Tk()
    app = App(root)  # Crea una instancia de la clase App
    root.mainloop()

if __name__ == '__main__':
    main()