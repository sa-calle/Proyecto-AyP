from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def imagen_de_fondo(ventana_principal):
    global fondo_imagen
    img = Image.open("E:/algoritmos y programacion/proyecto/IMG/FONDO.png")
    fondo_imagen = ImageTk.PhotoImage(img) 
    label_fondo = Label(ventana_principal, image=fondo_imagen)
  
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
        
def cerrar():
    ventana_principal.destroy()

def mostar(y_1):
    Label(ventasec,text=variable_parametros.get()).place(x=10,y=y_1)
    
def seguir():
    global ventasec,variable_parametros 
    ventasec=Toplevel()
    ventasec.title("Calculo")
    ventasec.geometry("862x517") 
    labelT=Label(ventasec,text='calculo' ,font=(' ',12,'bold'))
    labelT.place(x=10,y=10)
    parametros = ['uno', 'dos', 'tres', 'cuatro', 'cinco']
    variable_parametros = StringVar(ventasec, value='')
    y_1=50
    for parametro in parametros:
        radio_parametro = Radiobutton(ventasec, text=parametro, variable=variable_parametros, value=parametro)
        radio_parametro.place(x=10, y=y_1)
        y_1+=30
    bc=Button(ventasec,text='mostrar', command=lambda: mostar(y_1))
    y_1+=50
    bc.place(x=10,y=y_1)
    y_1+=30




#! -------------------------------------------------------------

def seleccionarop(tercera_ventana, opcion):
    if opcion == 'opcion 1':
        Label(tercera_ventana, text='La opción es:\t' + str(opcion)).pack()
    else:
        Label(tercera_ventana, text='Otra opción').pack()

def combos(tercera_ventana):
    parametros = ['opcion 1', 'opcion 2', 'opcion 3', 'opcion 4', 'opcion 5', 'otros']
    combobox = ttk.Combobox(tercera_ventana, values=parametros)
    combobox.bind('<<ComboboxSelected>>',
                  lambda event: seleccionarop(tercera_ventana, combobox.get()))
    combobox.pack(pady=10)

#!----------- menú popup -----------------------
    
def mostrar_mensaje():
    Label(tercera_ventana, text='Selección menú popup').pack()

def on_right_click(event):
    menu_emergente.post(event.x_root, event.y_root)
    
def menu_popup():
    global menu_emergente, tercera_ventana
    tercera_ventana = Toplevel()
    tercera_ventana.geometry("862x517")
    menu_emergente = Menu(tercera_ventana, tearoff=0)
    menu_emergente.add_command(label='Mostrar', command=mostrar_mensaje)
    menu_emergente.add_command(label='Viga 2', command=mostrar_mensaje)
    menu_emergente.add_command(label='Viga 3', command=mostrar_mensaje)
    menu_emergente.add_separator()
    menu_emergente.add_command(label='Salir', command=tercera_ventana.quit)
    tercera_ventana.bind('<Button-3>', on_right_click)
    combos(tercera_ventana)



