import tkinter as tk
from tkinter import messagebox
import subprocess
from model.productos_dao import crear_tabla, borrar_tabla
ventana = tk.Tk()
ventana.title("RJL PRODUCE WHOLESALE")
ventana.geometry("1400x500")
ventana.minsize(600,400)
ventana.iconbitmap("appBodega/image/bodeg.ico")
ventana.configure(bg="peach puff")

#aqui el contenido de la ventana
def registrarProducto():
    crear_tabla
    try:
        subprocess.run(["python", "appBodega/bdProductos.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def verVentas():
    try:
        subprocess.run(["python", "appBodega/registroVentas.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def imprimirRecibo():
    messagebox.showinfo("Imprimir Recibo", "Aquí se imprimirá el recibo.")
 

# Frame para el menú
menu_frame = tk.Frame(ventana, bg="peach puff")
menu_frame.pack(pady=25)

# Opción 1: Registrar Producto
img_registrar = tk.PhotoImage(file='appBodega/image/registrarProducto128.png')
lbl_registrar = tk.Label(menu_frame, image=img_registrar)
lbl_registrar.grid(row=1, column=0)
btnRegistrar = tk.Button(menu_frame, text="Registrar Producto", command=registrarProducto,bg="lightblue", font=("Arial", 14), width=20)
btnRegistrar.grid(row=2, column=0, padx=20)

# Opción 2: Ver Ventas
img_ver_ventas = tk.PhotoImage(file='appBodega/image/verVentas128.png')
lbl_ver_ventas = tk.Label(menu_frame, image=img_ver_ventas)
lbl_ver_ventas.grid(row=1, column=1)
btnVerVentas = tk.Button(menu_frame, text="Ver Ventas", command=verVentas,bg="lightgreen", font=("Arial", 14), width=20)
btnVerVentas.grid(row=2, column=1, padx=20)

# Opción 3: Imprimir Recibo
img_imprimir = tk.PhotoImage(file='appBodega/image/imprimir128.png')
lbl_imprimir = tk.Label(menu_frame, image=img_imprimir)
lbl_imprimir.grid(row=1, column=2)
btnImprimir = tk.Button(menu_frame, text="Imprimir Recibo", command=imprimirRecibo,bg="lightcoral", font=("Arial", 14), width=20)
btnImprimir.grid(row=2, column=2, padx=20)

#para que corra
ventana.mainloop()