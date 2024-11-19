from modulo_popup import menu_popup, combos, cerrar, mostar, imagen_de_fondo, seguir
from tkinter import *


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
                      command=seguir, bg='white', fg='black')
boton_seguir.place(x=720, y=470)


boton_menus = Button(ventana_principal, text='Menús', font=(' ', 12, 'bold'),
                     command=menu_popup, bg='white', fg='black')
boton_menus.place(x=650, y=470) 

ventana_principal.mainloop()
