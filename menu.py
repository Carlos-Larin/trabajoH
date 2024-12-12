import tkinter as tk
from tkinter import messagebox
import subprocess
from appBodega.model.productos_dao import crear_tabla

ventana = tk.Tk()
ventana.title("RJL PRODUCE WHOLESALE")
ventana.geometry("1400x500")
ventana.minsize(600, 400)
ventana.iconbitmap(r"C:/Users/PC/EmpresaH/appBodega/image/bodeg.ico")
ventana.configure(bg="peach puff")

# Función para registrar el producto
def registrarProducto():
    crear_tabla()  # Llamar correctamente la función de creación de tabla
    try:
        resultado = subprocess.run(["python", "C:/Users/PC/EmpresaH/appBodega/bdProductos.py"], check=True, capture_output=True, text=True)
        print(resultado.stdout)  # Ver la salida estándar del script
        print(resultado.stderr)  # Ver los errores estándar del script
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el script: {e}\n{e.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")


# Función para ver ventas
def verVentas():
    try:
        subprocess.run(["python", "C:/Users/PC/EmpresaH/appBodega/registroVentas.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el script: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

# Función para imprimir recibo
def imprimirRecibo():
    messagebox.showinfo("Imprimir Recibo", "Aquí se imprimirá el recibo.")

# Frame para el menú
menu_frame = tk.Frame(ventana, bg="peach puff")
menu_frame.pack(pady=25)

# Opción 1: Registrar Producto
img_registrar = tk.PhotoImage(file='C:/Users/PC/EmpresaH/appBodega/image/registrarProducto128.png')
lbl_registrar = tk.Label(menu_frame, image=img_registrar)
lbl_registrar.grid(row=1, column=0)
btnRegistrar = tk.Button(menu_frame, text="Registrar Producto", command=registrarProducto, bg="lightblue", font=("Arial", 14), width=20)
btnRegistrar.grid(row=2, column=0, padx=20)

# Opción 2: Ver Ventas
img_ver_ventas = tk.PhotoImage(file='C:/Users/PC/EmpresaH/appBodega/image/verVentas128.png')
lbl_ver_ventas = tk.Label(menu_frame, image=img_ver_ventas)
lbl_ver_ventas.grid(row=1, column=1)
btnVerVentas = tk.Button(menu_frame, text="Ver Ventas", command=verVentas, bg="lightgreen", font=("Arial", 14), width=20)
btnVerVentas.grid(row=2, column=1, padx=20)

# Para correr la ventana
ventana.mainloop()
