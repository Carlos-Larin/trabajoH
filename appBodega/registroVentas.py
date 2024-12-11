import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from model.ventas_dao import ver_ventas, borrar_venta, modificar_venta,obtener_precio_unitario


class RegistroVentas:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Ventas")
        self.root.geometry("800x600")
        self.root.iconbitmap("appBodega/image/bodeg.ico")

        self.frame = tk.Frame(root, bg="peach puff")
        self.frame.pack(pady=20)

        # Configuración de Treeview para mostrar ventas
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("ID Venta", "Cliente", "Productos", "Total", "Fecha")
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Encabezados de columnas
        
        self.tree["show"] = "headings"  # Mostrar encabezados
        self.tree.pack(pady=(10, 20), fill=tk.BOTH)  # Llenar el espacio disponible

        # Botones para acciones
        button_frame = tk.Frame(root, bg="peach puff")
        button_frame.pack(pady=(10, 20))

        btn_borrar = tk.Button(button_frame, text="Borrar Venta", command=self.borrar_venta)
        btn_borrar.grid(row=0, column=0, padx=10)

        btn_modificar = tk.Button(button_frame, text="Modificar Venta", command=self.modificar_venta)
        btn_modificar.grid(row=0, column=1, padx=10)

        btn_ver_ventas = tk.Button(button_frame, text="Ver Ventas", command=self.mostrar_ventas)
        btn_ver_ventas.grid(row=0, column=2, padx=10)

        btn_detalle_productos = tk.Button(button_frame, text="Detalle Productos", command=self.mostrar_detalles_productos)
        btn_detalle_productos.grid(row=0, column=3, padx=10)

        # Cargar y mostrar las ventas al iniciar
        self.mostrar_ventas()

    def mostrar_ventas(self):
        """Muestra las ventas almacenadas en el Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Limpia el Treeview antes de mostrar nuevos datos

        ventas = ver_ventas()  # Llama a la función para obtener ventas
        
        for v in ventas:
            productos_lista = v[2].split(',')
            productos_resumen = f"{len(productos_lista)} productos"
            self.tree.insert("", "end", values=(v[0], v[1], productos_resumen, f"${v[3]:.2f}", v[4]))

        # Ajustar el tamaño de las columnas para mejor visualización
        self.tree.column("ID Venta", width=100, anchor="center")
        self.tree.column("Cliente", width=150, anchor="center")
        self.tree.column("Productos", width=200, anchor="center")
        self.tree.column("Fecha", width=150, anchor="center")

    def mostrar_detalles_productos(self):
        """Muestra los detalles completos de los productos en una ventana emergente."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver los detalles de los productos.")
            return
        
        venta_id = self.tree.item(selected_item)["values"][0]  # Obtiene el ID de la venta seleccionada
        productos_completos = [venta for venta in ver_ventas() if venta[0] == venta_id][0][2]  # Encuentra la venta
        productos_formateados = "\n".join([producto.strip() for producto in productos_completos.split(',')])
        
        messagebox.showinfo("Detalle de Productos", f"Productos:\n\n{productos_formateados}")

    def borrar_venta(self):
        """Borra la venta seleccionada del Treeview y de la base de datos."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para borrar.")
            return
        
        venta_id = self.tree.item(selected_item)["values"][0]  # Obtiene el ID de la venta seleccionada
        
        borrar_venta(venta_id)  # Llama a la función para borrar la venta en la base de datos
        
        messagebox.showinfo("Éxito", f"Venta con ID {venta_id} ha sido borrada.")
        
        # Actualiza la visualización de ventas
        self.mostrar_ventas()

    def modificar_venta(self):
        """Modifica un producto de la venta seleccionada."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para modificar.")
            return
        
        venta_id = self.tree.item(selected_item)["values"][0]  # Obtiene el ID de la venta seleccionada
        venta_seleccionada = [venta for venta in ver_ventas() if venta[0] == venta_id][0]
        productos_completos = venta_seleccionada[2]
        cliente_nombre = venta_seleccionada[1]
        productos_lista = productos_completos.split(',')

        # Crear ventana emergente para seleccionar y modificar productos
        top = tk.Toplevel(self.root)
        top.title("Modificar Productos")
        top.geometry("400x400")

        label = tk.Label(top, text="Seleccione el producto a modificar:")
        label.pack(pady=10)

        # Tabla para mostrar productos
        product_tree = ttk.Treeview(top, columns=("Producto", "Cantidad", "Precio Unitario", "Total"), show="headings")
        product_tree.heading("Producto", text="Producto")
        product_tree.heading("Cantidad", text="Cantidad")
        product_tree.heading("Precio Unitario", text="Precio Unitario")
        product_tree.heading("Total", text="Total")
        product_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Rellenar la tabla con los productos
        for prod in productos_lista:
            nombre_producto = prod.strip()
            cantidad = 1  # Asignar una cantidad por defecto (puedes ajustar esto según tu lógica)
            precio_unitario = obtener_precio_unitario(nombre_producto)  # Obtener el precio unitario
            total_producto = cantidad * precio_unitario
            product_tree.insert("", "end", values=(nombre_producto, cantidad, f"${precio_unitario:.2f}", f"${total_producto:.2f}"))

        # Función para actualizar el total al cambiar la cantidad o el precio unitario
        def actualizar_total():
            for item in product_tree.get_children():
                item_values = product_tree.item(item)["values"]
                try:
                    nueva_cantidad = int(item_values[1])  # Obtener cantidad actual
                    precio_unitario = float(item_values[2].replace('$', '').replace(',', ''))  # Obtener precio unitario
                    nuevo_total = nueva_cantidad * precio_unitario
                    product_tree.item(item, values=(item_values[0], nueva_cantidad, f"${precio_unitario:.2f}", f"${nuevo_total:.2f}"))
                except ValueError:
                    pass

        # Función para editar la cantidad al hacer doble clic
        def on_double_click_cantidad(event):
            selected_product = product_tree.selection()
            if not selected_product:
                return
            
            item_values = product_tree.item(selected_product)["values"]
            old_quantity = item_values[1]  # Obtener cantidad actual
            
            new_quantity_str = simpledialog.askstring("Modificar Cantidad", f"Ingrese nueva cantidad para '{item_values[0]}':", initialvalue=old_quantity)
            
            if new_quantity_str is not None:
                try:
                    new_quantity = int(new_quantity_str)
                    product_tree.item(selected_product, values=(item_values[0], new_quantity,
                                                                item_values[2], 
                                                                f"${new_quantity * float(item_values[2].replace('$', '').replace(',', '')):.2f}"))
                    actualizar_total()  # Actualiza el total después de cambiar la cantidad
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")

        # Función para editar el precio unitario al hacer doble clic
        def on_double_click_precio(event):
            selected_product = product_tree.selection()
            if not selected_product:
                return
            
            item_values = product_tree.item(selected_product)["values"]
            old_price_str = item_values[2].replace('$', '').replace(',', '')  # Obtener precio actual
            
            new_price_str = simpledialog.askstring("Modificar Precio Unitario", f"Ingrese nuevo precio para '{item_values[0]}':", initialvalue=old_price_str)
            
            if new_price_str is not None:
                try:
                    new_price = float(new_price_str)
                    nueva_cantidad = int(item_values[1])  # Obtener cantidad actual
                    nuevo_total = nueva_cantidad * new_price
                    
                    product_tree.item(selected_product, values=(item_values[0], nueva_cantidad,
                                                                f"${new_price:.2f}", 
                                                                f"${nuevo_total:.2f}"))
                    actualizar_total()  # Actualiza el total después de cambiar el precio unitario
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese un precio válido.")

        # Asociar los eventos de doble clic a las funciones correspondientes
        product_tree.bind("<Double-1>", lambda event: on_double_click_cantidad(event) if product_tree.identify_column(event.x) == '#2' else on_double_click_precio(event) if product_tree.identify_column(event.x) == '#3' else None)

        # Botón para confirmar la modificación
        def confirmar_modificacion():
            selected_product = product_tree.selection()
            if not selected_product:
                messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
                return
            
            item_values = product_tree.item(selected_product)["values"]
            old_product_name = item_values[0]  # Producto seleccionado
            new_cantidad = item_values[1]  # Obtener nueva cantidad desde la tabla
            new_precio_unitario_str = item_values[2].replace('$', '').replace(',', '')  # Obtener nuevo precio unitario
            
            try:
                new_precio_unitario = float(new_precio_unitario_str)  # Convertir a float
                
                # Actualizar el producto en la lista con un formato legible
                productos_actualizados = [
                    f"{old_product_name.strip()} (Cantidad: {new_cantidad}, Precio: ${new_precio_unitario})"
                    for prod in productos_lista if prod.strip() == old_product_name.strip()
                ]
                modificar_venta(venta_id, cliente_nombre, ",".join(productos_actualizados))  # Mantener cliente existente
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.mostrar_ventas()  # Actualiza la lista de ventas
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un valor válido.")

        # Botón para confirmar la modificación
        btn_confirmar = tk.Button(top, text="Confirmar Modificación", command=confirmar_modificacion)
        btn_confirmar.pack(pady=10)

        # Botón para cerrar la ventana sin realizar cambios
        btn_cancelar = tk.Button(top, text="Cancelar", command=top.destroy)
        btn_cancelar.pack(pady=5)

        # Mantener el flujo de la ventana emergente
        top.grab_set()



def main():
    root = tk.Tk()
    app = RegistroVentas(root)  # Crea una instancia de la clase RegistroVentas
    root.mainloop()


if __name__ == '__main__':
    main()
