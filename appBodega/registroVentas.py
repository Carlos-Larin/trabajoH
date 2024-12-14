import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from model.ventas_dao import ver_ventas, borrar_venta, insertar_venta
import smtplib
from email.message import EmailMessage
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        self.set_font("Arial", size=12, style="B")
        self.cell(0, 10, "Invoice", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

class RegistroVentas:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Ventas")
        self.root.geometry("800x600")
        self.root.iconbitmap(r"C:/Users/PC/EmpresaH/appBodega/image/bodeg.ico")
        
        self.frame = tk.Frame(root, bg="peach puff")
        self.frame.pack(pady=20)

        # Credenciales de correo
        self.correo_usuario = "trabajoh060904@gmail.com"  # Correo proporcionado
        self.contrasena_usuario = "qscq dbxk urnq sbev"  # Contraseña proporcionada

        # Configuración de Treeview para mostrar ventas
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("ID Venta", "Cliente", "Direccion", "Productos", "Total", "Fecha")
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        
        self.tree["show"] = "headings"
        self.tree.pack(pady=(10, 20), fill=tk.BOTH)

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
            self.tree.delete(row)
        
        ventas = ver_ventas()
        
        for v in ventas:
            try:
                # Validar y mostrar dirección correctamente
                direccion = v[2] if v[2] else "Sin dirección"
                
                # Procesar productos
                productos_lista = v[3].split(',') if v[3] else []
                productos_resumen = f"{len(productos_lista)} productos"
                
                # Convertir total a formato numérico si es necesario
                total = float(v[4]) if isinstance(v[4], (int, float)) else 0.0
                total_formatted = f"${total:.2f}"
                
                # Insertar datos en el Treeview
                self.tree.insert("", "end", values=(v[0], v[1], direccion, productos_resumen, total_formatted, v[5]))
            except Exception as e:
                print(f"Error procesando venta {v[0]}: {e}")

    def mostrar_detalles_productos(self):
        """Muestra los detalles completos de los productos en una ventana emergente."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver los detalles de los productos.")
            return
        
        venta_id = self.tree.item(selected_item)["values"][0]
        
        productos_completos = [venta for venta in ver_ventas() if venta[0] == venta_id][0][3]
        
        detalles = []
        
        for producto in productos_completos.split(','):
            try:
                partes = producto.strip().split('x')
                if len(partes) == 2:
                    nombre_producto = partes[0].strip()
                    cantidad_info = partes[1].strip().split('(')
                    if len(cantidad_info) == 2:
                        cantidad = float(cantidad_info[0].strip())
                        precio_total = float(cantidad_info[1].strip(')').strip('$'))
                        precio_unitario = precio_total / cantidad
                        detalles.append(f"{nombre_producto} (Cantidad: {cantidad:.2f}, Precio unitario: ${precio_unitario:.2f}, Total: ${precio_total:.2f})")
                    else:
                        detalles.append(f"{producto} ( falta el precio)")
                else:
                    detalles.append(f"{producto} ( falta 'x')")
            except Exception as e:
                detalles.append(f"{producto} (Error: {str(e)})")

        messagebox.showinfo("Detalle de Productos", f"Productos:\n\n" + "\n".join(detalles))

    def borrar_venta(self):
        """Borra la venta seleccionada del Treeview y de la base de datos."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para borrar.")
            return
        
        venta_id = self.tree.item(selected_item)["values"][0]
        
        borrar_venta(venta_id)
        
        messagebox.showinfo("Éxito", f"Venta con ID {venta_id} ha sido borrada.")
        
        self.mostrar_ventas()

    def generar_pdf(self,direccion, venta_id, cliente, productos, total, fecha):
        """Genera un PDF con los detalles de la venta."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)


        # Título del recibo
        pdf.cell(200, 10, txt="1100 OMAHA DR", ln=True, align='C')
        pdf.cell(200, 10, txt="NORCROSS GA 30093", ln=True, align='C')
        pdf.ln(10)

        # Información de la venta
        pdf.cell(200, 10, txt=f"ID Venta: {venta_id}", ln=True)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
        pdf.cell(200, 10, txt=f"Bill to: {direccion}", ln=True)
        pdf.ln(10)

        # Detalles de los productos
        pdf.cell(200, 10, txt="Detalles de los Productos:", ln=True)
        pdf.ln(5)

        # Cabecera de la tabla
        pdf.set_font("Arial", size=10, style="B")
        pdf.cell(80, 10, "Producto", border=1, align="C")
        pdf.cell(40, 10, "Cantidad", border=1, align="C")
        pdf.cell(40, 10, "Precio", border=1, align="C")
        pdf.cell(40, 10, "Subtotal", border=1, align="C")
        pdf.ln()

        # Procesar productos
        pdf.set_font("Arial", size=10)
        subtotal_total = 0.0

        for producto in productos.split(','):
            partes = producto.split('x')  # Suponiendo que el formato es "producto x cantidad (precio)"
            if len(partes) == 2:
                nombre = partes[0].strip()
                cantidad_y_precio = partes[1].strip().split('(')

                if len(cantidad_y_precio) == 2:
                    try:
                        cantidad = float(cantidad_y_precio[0].strip())
                        precio_total = float(cantidad_y_precio[1].strip(')').strip('$'))
                        precio_unitario = precio_total / cantidad
                        subtotal_total += precio_total

                        # Imprimir datos del producto en la tabla
                        pdf.cell(80, 10, txt=nombre[:80], border=1)  # Limitar a 80 caracteres
                        pdf.cell(40, 10, txt=f"{cantidad:.2f}", border=1, align="C")
                        pdf.cell(40, 10, txt=f"${precio_unitario:.2f}", border=1, align="C")
                        pdf.cell(40, 10, txt=f"${precio_total:.2f}", border=1, align="C")
                        pdf.ln()
                    except ValueError:
                        pdf.cell(200, 10, txt=f"Error en formato para el producto: {producto}", ln=True)
                else:
                    pdf.cell(200, 10, txt=f"Formato inválido para el producto: {producto}", ln=True)
            else:
                pdf.cell(200, 10, txt=f"Formato inválido para el producto: {producto}", ln=True)

        # Total final
        pdf.ln(5)
        pdf.set_font("Arial", size=12, style="B")
        pdf.cell(160, 10, txt="Total:", align='R')
        pdf.cell(40, 10, txt=f"${subtotal_total:.2f}", border=1, align="C")

        # Guardar el PDF
        pdf_file = f"recibo_{venta_id}.pdf"
        pdf.output(pdf_file)

        return pdf_file



    def enviarRecibo(self):
        """Genera un PDF del recibo y lo envía por correo."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una venta para enviar el recibo.")
            return

        # Obtener los valores de la venta seleccionada
        values = self.tree.item(selected_item)["values"]
        print(values)  # Agregar esto para verificar el contenido exacto
        
        # Desempaquetar los valores correctamente
        try:
            venta_id, cliente, direccion, productos_completos_str, total_str, fecha = values
        except ValueError as e:
            messagebox.showerror("Error", f"Error al procesar los valores: {e}")
            return

        # Obtener los productos completos
        productos_completos = [venta for venta in ver_ventas() if venta[0] == venta_id][0][3]

        # Generar el PDF
        pdf_file = self.generar_pdf(direccion,venta_id, cliente, productos_completos, total_str.strip(), fecha)

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
                file_name = f"recibo_{venta_id}.pdf"
            
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

            # Configura tu servidor SMTP
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.correo_usuario, self.contrasena_usuario)
                server.send_message(msg)

            messagebox.showinfo("Éxito", "Recibo enviado correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroVentas(root)
    root.mainloop()
