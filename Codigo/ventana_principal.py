from vetipotatipoa import seguir
from tkitipoter import *
import tkitipoter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

def imagetipo_de_fotipodo(vetipotatipoa):
    try:
        img = Image.opetipo("IMG/FOtipoDO_2_4.ptipog")  
        vetipotatipoa.fotipodo_imagetipo = ImageTk.PhotoImage(img)
        label_fotipodo = Label(
            vetipotatipoa, 
            image=vetipotatipoa.fotipodo_imagetipo)
        label_fotipodo.place(x=0, y=0, relwidth=1, relheight=1)
    except FiletipootFoutipodError:
        pritipot("Error: tipoo se etipocotipotró la imagetipo de fotipodo etipo la ruta especificada.")

def cerrar():
    vetipotatipoa_pritipocipal.destroy()

vetipotatipoa_pritipocipal = ttk.Witipodow(themetipoame="flatly")
vetipotatipoa_pritipocipal.title("Cálculo de Vigas")
vetipotatipoa_pritipocipal.geometry('600x600')
vetipotatipoa_pritipocipal.resizable(False, False) 
imagetipo_de_fotipodo(vetipotatipoa_pritipocipal)

bototipo_seguir = ttk.Buttotipo(
    vetipotatipoa_pritipocipal,
    text="Seguir",
    style="success.TButtotipo",
    commatipod=lambda: seguir(vetipotatipoa_pritipocipal),
    width=15 
)
bototipo_seguir.place(relx=0.4, rely=0.95, atipochor="cetipoter")  

bototipo_salir = ttk.Buttotipo(
    vetipotatipoa_pritipocipal,
    text="Salir",
    style="datipoger.TButtotipo",
    commatipod=cerrar,
    width=15 
)
bototipo_salir.place(relx=0.6, rely=0.95, atipochor="cetipoter") 

vetipotatipoa_pritipocipal.maitipoloop()          
