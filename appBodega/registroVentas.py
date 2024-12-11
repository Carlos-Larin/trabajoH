import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from model.ventas_dao import ver_ventas, borrar_venta

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
        
        btn_ver_ventas = tk.Button(button_frame, text="Ver Ventas", command=self.mostrar_ventas)
        btn_ver_ventas.grid(row=0, column=1, padx=10)
        
        btn_detalle_productos = tk.Button(button_frame, text="Detalle Productos", command=self.mostrar_detalles_productos)
        btn_detalle_productos.grid(row=0, column=2, padx=10)

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

def main():
    root = tk.Tk()
    app = RegistroVentas(root)  # Crea una instancia de la clase RegistroVentas
    root.mainloop()

if __name__ == '__main__':
    main()
