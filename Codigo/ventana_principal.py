from ventana import seguir
from tkinter import *
import tkinter as tk
import ttkbootstrap as ttk 
from PIL import Image, ImageTk

def imagen_de_fondo(ventana_principal):
    global fondo_imagen
    img = Image.open("IMG\FONDO_2.png")
    fondo_imagen = ImageTk.PhotoImage(img) 
    label_fondo = Label(ventana_principal, image=fondo_imagen)
  
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

def cerrar():
    ventana_principal.destroy()
#------------------------ventana principal---------------------------------------------------------   

ventana_principal = ttk.Window(themename="flatly") 
ventana_principal.title("CALCULO DE VIGAS")
ventana_principal.geometry('600x900')
imagen_de_fondo(ventana_principal)

#----------------------------------------botones--------------------------------------------------------


boton_salir = ttk.Button(ventana_principal, text='Salir',style="danger.TButton",
                     command=lambda: cerrar(ventana_principal))
boton_salir.place(x=790, y=470) 

boton_seguir = ttk.Button(ventana_principal, text='Seguir',style="success.TButton",
                      command=lambda: seguir(ventana_principal))
boton_seguir.place(x=720, y=470)

ventana_principal.mainloop()

