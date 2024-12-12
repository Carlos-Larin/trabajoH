import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from model.productos_dao import crear_tabla, insertar_producto, ver_productos, borrar_producto, modificar_producto
from model.ventas_dao import crear_tabla_ventas, insertar_venta

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RJL BDProductos")
        self.root.geometry("900x700")

        try:
            self.root.iconbitmap("appBodega/image/bodeg.ico")
        except Exception:
            print("Icono no encontrado. Se usará el predeterminado.")

        crear_tabla()
        crear_tabla_ventas()

        self.frame = tk.Frame(root, bg="peach puff")
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Nombre del Cliente:", bg="peach puff").grid(row=0, column=0, padx=10, pady=10)
        self.entry_cliente = tk.Entry(self.frame)
        self.entry_cliente.grid(row=0, column=1)

        button_frame = tk.Frame(root, bg="peach puff")
        button_frame.pack(pady=(10, 20))

        tk.Button(button_frame, text="Ver Productos", command=self.mostrar_productos).grid(row=0, column=0, padx=(5, 10))
        tk.Button(button_frame, text="Agregar Producto", command=self.agregar_producto).grid(row=0, column=1, padx=(5, 10))
        tk.Button(button_frame, text="Agregar a Venta", command=self.agregar_a_venta).grid(row=0, column=2, padx=(5, 10))
        tk.Button(button_frame, text="Modificar Producto", command=self.modificar_producto).grid(row=0, column=3, padx=(5, 10))
        tk.Button(button_frame, text="Borrar Producto", command=self.borrar_producto).grid(row=0, column=4, padx=(5, 10))

        self.tree = ttk.Treeview(root, selectmode="none")
        self.tree["columns"] = ("Seleccionar", "ID", "Nombre", "Precio Unitario", "Cantidad", "Subtotal")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.tree.column("Seleccionar", width=80, anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150, anchor="w")
        self.tree.column("Precio Unitario", width=100, anchor="center")
        self.tree.column("Cantidad", width=100, anchor="center")
        self.tree.column("Subtotal", width=100, anchor="center")

        self.tree["show"] = "headings"
        self.tree.pack(pady=(10, 20), fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.editar_cantidad)
        self.tree.bind("<Button-1>", self.toggle_seleccion)

        self.total_label = tk.Label(root, text="Total a pagar: $0.00", font=("Arial", 14), bg="peach puff")
        self.total_label.pack(anchor="e", padx=20, pady=(0, 20))

        self.productos_seleccionados = {}

    def editar_cantidad(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        valores = self.tree.item(item_id, "values")
        if not valores:
            return
        
        # Mostrar un cuadro de diálogo para ingresar la nueva cantidad
        try:
            nueva_cantidad = simpledialog.askinteger("Editar Cantidad", "Ingrese la nueva cantidad:", initialvalue=valores[4])
            
            if nueva_cantidad is None:  # El usuario canceló la entrada
                return
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            
            # Actualizar la base de datos
            producto_id = valores[1]  # Columna de ID
            modificar_producto(producto_id, valores[1], valores[2], nueva_cantidad, valores[3])  # Actualizar en la base de datos
            
            # Calcular subtotal
            precio_unitario = float(valores[3])
            subtotal = nueva_cantidad * precio_unitario
            
            # Actualizar el elemento en Treeview
            self.tree.item(item_id, values=(valores[0], valores[1], valores[2], f"{precio_unitario:.2f}", nueva_cantidad, f"{subtotal:.2f}"))
            
            # Actualizar los datos seleccionados
            self.productos_seleccionados[item_id]["cantidad"] = nueva_cantidad
            self.productos_seleccionados[item_id]["subtotal"] = subtotal
            
            # Recalcular total inmediatamente después de actualizar la cantidad
            self.calcular_total()
        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {e}")



    def mostrar_productos(self):
        self.tree.delete(*self.tree.get_children())
        try:
            productos = ver_productos()
            for p in productos:
                item_id = self.tree.insert("", "end", values=("No", p[0], p[1], f"{p[3]:.2f}", 0, 0))
                self.productos_seleccionados[item_id] = {
                    "seleccionado": False,
                    "cantidad": 0,
                    "subtotal": 0.0,
                    "precio_unitario": p[3]
                }
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")

    def toggle_seleccion(self, event):
        column = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        if column == "#1" and item_id:
            current_value = self.tree.set(item_id, "Seleccionar")
            new_value = "Sí" if current_value == "No" else "No"
            self.tree.set(item_id, "Seleccionar", new_value)
            self.productos_seleccionados[item_id]["seleccionado"] = (new_value == "Sí")

    def agregar_producto(self):
        producto_popup = tk.Toplevel(self.root)
        producto_popup.title("Agregar Producto")

        tk.Label(producto_popup, text="ID del Producto:").grid(row=0, column=0, pady=5, padx=5)
        entry_id = tk.Entry(producto_popup)
        entry_id.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(producto_popup, text="Nombre del Producto:").grid(row=1, column=0, pady=5, padx=5)
        entry_nombre = tk.Entry(producto_popup)
        entry_nombre.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(producto_popup, text="Precio Unitario:").grid(row=2, column=0, pady=5, padx=5)
        entry_precio = tk.Entry(producto_popup)
        entry_precio.grid(row=2, column=1, pady=5, padx=5)

        # Se elimina la sección de entrada de cantidad
        # tk.Label(producto_popup, text="Cantidad:").grid(row=3, column=0, pady=5, padx=5)
        # entry_cantidad = tk.Entry(producto_popup)
        # entry_cantidad.grid(row=3, column=1, pady=5, padx=5)

        def guardar_producto():
            try:
                producto_id = entry_id.get().strip()
                nombre = entry_nombre.get().strip()
                precio = float(entry_precio.get())
                # La cantidad se puede definir aquí si es necesario establecer un valor por defecto
                cantidad = 0  # O puedes establecer otro valor por defecto si lo prefieres

                if not producto_id or not nombre or precio <= 0 or cantidad < 0:
                    raise ValueError("Datos inválidos.")

                productos_existentes = [p[0] for p in ver_productos()]
                if producto_id in productos_existentes:
                    raise ValueError("El ID del producto ya existe.")

                insertar_producto(producto_id, nombre, precio, cantidad)  # Se usa la cantidad definida
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                producto_popup.destroy()
                self.mostrar_productos()

            except ValueError as e:
                messagebox.showerror("Error", f"{e}")

        tk.Button(producto_popup, text="Guardar", command=guardar_producto).grid(row=4, columnspan=2, pady=10)


    def calcular_total(self):
        total = sum(prod["subtotal"] for prod in self.productos_seleccionados.values() if prod["seleccionado"])
        self.total_label.config(text=f"Total a pagar: ${total:.2f}")

    def agregar_a_venta(self):
        """Agrega los productos seleccionados a una venta."""
        cliente_nombre = self.entry_cliente.get().strip()
        if not cliente_nombre:
            messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del cliente.")
            return

        productos_a_vender = []
        total_venta = 0.0
        for item_id in self.tree.get_children():
            # Verifica si el producto está seleccionado
            if self.tree.item(item_id)["values"][0] == "Sí":  # Solo procesa si está seleccionado
                nombre = self.tree.item(item_id)["values"][2]  # Nombre del producto
                try:
                    cantidad = float(self.tree.item(item_id)["values"][4])  # Acepta cantidades decimales
                    if cantidad <= 0:
                        raise ValueError("La cantidad debe ser mayor que cero.")
                    precio_unitario = float(self.tree.item(item_id)["values"][3].replace('$', '').replace(',', ''))
                    subtotal = precio_unitario * cantidad
                    total_venta += subtotal
                    productos_a_vender.append(f"{nombre} x {cantidad:.2f} (${subtotal:.2f})")
                except ValueError as e:
                    messagebox.showerror("Error", f"Error al procesar el producto '{nombre}': {e}")
                    return

        # Verifica si se han agregado productos a la lista
        if not productos_a_vender:
            messagebox.showwarning("Advertencia", "No se han seleccionado productos para la venta.")
            return

        # Convertir la lista de productos a una cadena
        productos_str = ', '.join(productos_a_vender)

        # Llamar a insertar_venta con los productos formateados y el total calculado
        insertar_venta(cliente_nombre, productos_str, total_venta)

        messagebox.showinfo("Éxito", f"Venta registrada para {cliente_nombre}:\n{productos_str}\nTotal: ${total_venta:.2f}")
        # Limpiar entradas y Treeview
        self.entry_cliente.delete(0, tk.END)
        self.mostrar_productos()




    def modificar_producto(self):
        item_id = self.tree.focus()
        if not item_id:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para modificar.")
            return

        valores = self.tree.item(item_id, "values")
        if not valores:
            return

        producto_popup = tk.Toplevel(self.root)
        producto_popup.title("Modificar Producto")

        tk.Label(producto_popup, text="ID del Producto:").grid(row=0, column=0, pady=5, padx=5)
        entry_id = tk.Entry(producto_popup)
        entry_id.insert(0, valores[1])
        entry_id.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(producto_popup, text="Nombre del Producto:").grid(row=1, column=0, pady=5, padx=5)
        entry_nombre = tk.Entry(producto_popup)
        entry_nombre.insert(0, valores[2])
        entry_nombre.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(producto_popup, text="Precio Unitario:").grid(row=2, column=0, pady=5, padx=5)
        entry_precio = tk.Entry(producto_popup)
        entry_precio.insert(0, valores[3])
        entry_precio.grid(row=2, column=1, pady=5, padx=5)

        def guardar_cambios():
            try:
                nuevo_id = entry_id.get().strip()
                nombre = entry_nombre.get().strip()
                precio = float(entry_precio.get())

                if not nuevo_id or not nombre or precio <= 0:
                    raise ValueError("Datos inválidos.")

                producto_original_id = valores[1]  # El ID original del producto seleccionado

                if nuevo_id != producto_original_id:
                    productos_existentes = [p[0] for p in ver_productos()]
                    if nuevo_id in productos_existentes:
                        raise ValueError("El nuevo ID del producto ya existe.")

                cantidad_actual = int(valores[4])  # La cantidad no se modifica, se toma directamente del Treeview
                subtotal = precio * cantidad_actual  # Recalcular el subtotal

                modificar_producto(producto_original_id, nuevo_id, nombre, cantidad_actual, precio)
                self.tree.item(item_id, values=("No", nuevo_id, nombre, f"{precio:.2f}", cantidad_actual, f"{subtotal:.2f}"))

                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                producto_popup.destroy()
                self.calcular_total()

            except ValueError as e:
                messagebox.showerror("Error", f"{e}")

        tk.Button(producto_popup, text="Guardar Cambios", command=guardar_cambios).grid(row=3, columnspan=2, pady=10)

    def borrar_producto(self):
        item_id = self.tree.focus()
        if not item_id:
            messagebox.showerror("Error", "Seleccione un producto para borrar.")
            return

        producto_id = self.tree.set(item_id, "ID")
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar este producto?"):
            borrar_producto(producto_id)
            messagebox.showinfo("Éxito", "Producto borrado correctamente.")
            self.mostrar_productos()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
