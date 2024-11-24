from ventana import seguir
from tkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

def imagen_de_fondo(ventana):
    try:
        img = Image.open("IMG/FONDO_2_4.png")  
        ventana.fondo_imagen = ImageTk.PhotoImage(img)
        label_fondo = Label(
            ventana, 
            image=ventana.fondo_imagen)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Error: No se encontró la imagen de fondo en la ruta especificada.")

def cerrar():   
    ventana_principal.destroy()     

ventana_principal = ttk.Window(themename="flatly")
ventana_principal.title("Cálculo de Vigas")
ventana_principal.geometry('600x600')
ventana_principal.resizable(False, False)
ventana_principal.protocol("WM_DELETE_WINDOW", cerrar) 
imagen_de_fondo(ventana_principal)
boton_seguir = ttk.Button(
    ventana_principal,
    text="Seguir",
    style="success.TButton",
    command=lambda: seguir(ventana_principal),
    width=15 
)
boton_seguir.place(relx=0.4, rely=0.95, anchor="center")  

boton_salir = ttk.Button(
    ventana_principal,
    text="Salir",
    style="danger.TButton",
    command=cerrar,
    width=15 
)
boton_salir.place(relx=0.6, rely=0.95, anchor="center") 

ventana_principal.mainloop()          
