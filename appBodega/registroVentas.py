import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from model.ventas_dao import ver_ventas, borrar_venta, insertar_venta
import smtplib
from email.message import EmailMessage
from fpdf import FPDF

class RegistroVentas:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Ventas")
        self.root.geometry("800x600")
        self.root.iconbitmap("appBodega/image/bodeg.ico")
        self.frame = tk.Frame(root, bg="peach puff")
        self.frame.pack(pady=20)

        # Credenciales de correo
        self.correo_usuario = "trabajoh060904@gmail.com"  # Correo proporcionado
        self.contrasena_usuario = "qscq dbxk urnq sbev"  # Contraseña proporcionada

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

        btn_enviarRecibo = tk.Button(button_frame, text="Enviar Recibo", command=self.enviarRecibo)
        btn_enviarRecibo.grid(row=0, column=3, padx=10)

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
        detalles = []
        for producto in productos_completos.split(','):
            partes = producto.strip().split('x')
            if len(partes) == 2:
                nombre_producto = partes[0].strip()
                cantidad_info = partes[1].strip().split('(')
                if len(cantidad_info) == 2:
                    cantidad = cantidad_info[0].strip()
                    precio_total = cantidad_info[1].strip(')').strip('$')
                    try:
                        cantidad = float(cantidad)
                        precio_total = float(precio_total)
                        precio_unitario = precio_total / cantidad
                        detalles.append(f"{nombre_producto} (Cantidad: {cantidad:.2f}, Precio unitario: ${precio_unitario:.2f}, Total: ${precio_total:.2f})")
                    except ValueError:
                        detalles.append(f"{producto} (Error en formato numérico)")
                else:
                    detalles.append(f"{producto} (Formato inválido)")
            else:
                detalles.append(f"{producto} (Formato inválido)")

        messagebox.showinfo("Detalle de Productos", f"Productos:\n\n" + "\n".join(detalles))

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

    def generar_pdf(self, venta_id, cliente, productos, total, fecha):
            """Genera un PDF con los detalles de la venta."""
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Recibo de Venta", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"ID Venta: {venta_id}", ln=True)
            pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
            pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt="Detalles de los Productos:", ln=True)
            pdf.ln(5)
            for producto in productos.split(','):
                partes = producto.split(':')
                if len(partes) == 3:
                    nombre, cantidad, precio = partes
                    try:
                        cantidad = float(cantidad)
                        precio = float(precio)
                        subtotal = cantidad * precio
                        pdf.cell(200, 10, txt=f"{nombre} - Cantidad: {cantidad}, Precio: ${precio:.2f}, Subtotal: ${subtotal:.2f}", ln=True)
                    except ValueError:
                        pdf.cell(200, 10, txt=f"{producto} (Error de formato en los valores numéricos)", ln=True)
                else:
                    pdf.cell(200, 10, txt=f"{producto} (Formato inválido)", ln=True)

            pdf.ln(10)
            try:
                total_float = float(str(total).replace('$', '').replace(',', ''))
                pdf.cell(200, 10, txt=f"Total: ${total_float:.2f}", ln=True)
            except ValueError:
                pdf.cell(200, 10, txt=f"Total: {total} (Error en formato)", ln=True)


            pdf_file = f"recibo_{venta_id}.pdf"
            pdf.output(pdf_file)
            return pdf_file


    def enviarRecibo(self):
        """Genera un PDF del recibo y lo envía por correo."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para enviar el recibo.")
            return

        values = self.tree.item(selected_item)["values"]
        venta_id, cliente, productos, total, fecha = values
        productos_completos = [venta for venta in ver_ventas() if venta[0] == venta_id][0][2]

        # Generar el PDF
        pdf_file = self.generar_pdf(venta_id, cliente, productos_completos, total, fecha)

        # Solicitar correo del cliente
        correo_cliente = simpledialog.askstring("Enviar Recibo", "Ingrese el correo del cliente:")
        if not correo_cliente:
            messagebox.showwarning("Advertencia", "No se ingresó un correo válido.")
            return

        # Enviar el PDF por correo
        try:
            msg = EmailMessage()
            msg['Subject'] = f"Recibo de Venta ID {venta_id}"
            msg['From'] = self.correo_usuario
            msg['To'] = correo_cliente
            msg.set_content("Adjunto encontrará el recibo de su compra. Gracias por su preferencia.")

            with open(pdf_file, "rb") as f:
                file_data = f.read()
                file_name = pdf_file
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

            # Configura tu servidor SMTP
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.correo_usuario, self.contrasena_usuario)
                server.send_message(msg)

            messagebox.showinfo("Éxito", "Recibo enviado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {e}")




def main():
    root = tk.Tk()
    app = RegistroVentas(root)  # Crea una instancia de la clase RegistroVentas
    root.mainloop()

if __name__ == '__main__':
    main()

