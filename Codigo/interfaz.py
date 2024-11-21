from ventana import seguir
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def imagen_de_fondo(ventana_principal):
    global fondo_imagen
    img = Image.open("IMG\FONDO.png")
    fondo_imagen = ImageTk.PhotoImage(img) 
    label_fondo = Label(ventana_principal, image=fondo_imagen)
  
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

def cerrar():
    ventana_principal.destroy()
#------------------------ventana principal---------------------------------------------------------   

ventana_principal = Tk()
ventana_principal.title("NOMBRE DEL PROYECTO")
ventana_principal.geometry('862x517')
imagen_de_fondo(ventana_principal)

#----------------------------------------botones--------------------------------------------------------
boton_salir = Button(ventana_principal, text='Salir', font=(' ', 12, 'bold'),
                     command=lambda: cerrar(ventana_principal), bg='white', fg='black')
boton_salir.place(x=790, y=470)

boton_seguir = Button(ventana_principal, text='Seguir', font=(' ', 12, 'bold'),
                      command=lambda: seguir(ventana_principal), bg='white', fg='black')
boton_seguir.place(x=720, y=470)

ventana_principal.mainloop()
