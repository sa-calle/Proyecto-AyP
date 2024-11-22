import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk 
import matplotlib.pyplot as plt
import numpy as np

def seguir(ventana_principal):
    ventana_principal.destroy()

    longitud_viga = 10
    datos = []  

    def graficar_viga(datos, long, material, tipo_de_viga, x_apoyo_fijo=None, x_apoyo_pat=None):
        altura_viga = 0.01 * long

        if material == "Madera":
            color_viga = '#8A4C29' 
        elif material == "Acero":
            color_viga = '#B0C4DE' 
        elif material == "Concreto":
            color_viga = '#A9A9A9'  
        else:
            color_viga = '#8A4C29' 

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.set_xlim(-0.1 * long, 1.1 * long)
        ax.set_ylim(-2 * altura_viga, 3 * altura_viga)

        rect = plt.Rectangle((0, 0), long, altura_viga, color=color_viga)
        ax.add_patch(rect)

        if tipo_de_viga == "Viga en voladizo":
            ax.plot([0, 0], [0, altura_viga * 2], color='black', linewidth=2)
        elif tipo_de_viga == "Doblemente empotrada":
            ax.plot([0, 0], [0, altura_viga * 2], color='black', linewidth=2)
            ax.plot([long, long], [0, altura_viga * 2], color='black', linewidth=2)
        elif tipo_de_viga == "Simplemente apoyada":
            if x_apoyo_fijo is not None:
                ax.plot(x_apoyo_fijo, -altura_viga*0.4 , marker='^', color='black', markersize=15)
            if x_apoyo_pat is not None:
                ax.plot(x_apoyo_pat, -altura_viga*0.4 , marker='o', color='black', markersize=15)

        for carga, x in datos:
            if carga > 0:
                y_inicial = altura_viga
                dy = 1
            else:
                y_inicial = 0
                dy = -1

            ax.arrow(x, y_inicial, 0, dy * altura_viga, width=0.05,
                    head_width=0.2, head_length=0.07, fc='black', ec='black')

            ax.text(
                x, y_inicial + dy * 2.1 * altura_viga,
                f'{carga}N', ha='center', va='bottom' if dy > 0 else 'top',
                color='black'
            )

        ax.set_xlabel('Longitud de la viga (m)')
        ax.axis('off')
        plt.show()

    def obtener_datos():
        global longitud_viga  

        try:
            tipo_de_viga = tipo_viga_var.get()  
            longitud_viga_input = longitud_viga_var.get()
            material = material_var.get()  

            if not longitud_viga_input:
                raise ValueError("La longitud de la viga no puede estar vacía.")
            longitud_viga = float(longitud_viga_input)

            x_apoyo_pat, x_apoyo_fijo = None, None
            if tipo_de_viga == "Simplemente apoyada":
                tipo_de_viga = "Simplemente apoyada"
                x_apoyo_pat = float(entry_apoyo_pat.get())
                x_apoyo_fijo = float(entry_apoyo_fijo.get())
                if not (0 <= x_apoyo_pat <= longitud_viga) or not (0 <= x_apoyo_fijo <= longitud_viga):
                    raise ValueError("Las coordenadas de los apoyos deben estar dentro de la longitud de la viga.")
            elif tipo_de_viga == "Viga en voladizo":
                tipo_de_viga = "Viga en voladizo"
            elif tipo_de_viga == "Doblemente empotrada":
                tipo_de_viga = "Doblemente empotrada"
            else:
                raise ValueError("Tipo de viga inválido.")

            datos_viga = f"Tipo de viga: {tipo_de_viga}\nLongitud de la viga: {longitud_viga} m\nMaterial: {material}\n\n"
            datos_fuerzas = "Fuerzas ingresadas:\n"
            
            if not datos:
                datos_fuerzas += "No se han ingresado fuerzas."
            else:
                for fuerza in datos:
                    datos_fuerzas += f"Carga: {fuerza[0]} N, Coordenada x: {fuerza[1]} m\n"
            
            mensaje = datos_viga + datos_fuerzas
            messagebox.showinfo("Datos de la Viga y Fuerzas", mensaje)

            mostrar_grafico(x_apoyo_fijo, x_apoyo_pat, tipo_de_viga)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_fuerza():
        try:
            global longitud_viga  
            longitud_viga = float(longitud_viga_var.get())  
            
            carga = float(entry_carga.get())
            x = float(entry_x.get())

            if not (0 <= x <= longitud_viga):
                raise ValueError(f"La coordenada x debe estar entre 0 y {longitud_viga}.")

            datos.append([carga, x])
            messagebox.showinfo("Fuerza Agregada", "Fuerza agregada correctamente.")

            entry_carga.delete(0, tk.END)
            entry_x.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def borrar_fuerzas():
        global datos
        if not datos:
            messagebox.showwarning("Advertencia", "No hay fuerzas para borrar.")
        else:
            datos.clear()  
            messagebox.showinfo("Fuerzas Borradas", "Las fuerzas ingresadas han sido borradas.")

    def mostrar_grafico(x_apoyo_fijo=None, x_apoyo_pat=None, tipo_de_viga=None):
        material = material_var.get()
        tipo_de_viga = tipo_viga_var.get()

        graficar_viga(datos, longitud_viga, material, tipo_de_viga, x_apoyo_fijo, x_apoyo_pat)

    def mostrar_campos_apoyos(*args):
        if tipo_viga_var.get() == "Simplemente apoyada":
            label_apoyo_pat.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            entry_apoyo_pat.grid(row=3, column=1, padx=5, pady=5)
            label_apoyo_fijo.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            entry_apoyo_fijo.grid(row=4, column=1, padx=5, pady=5)
        else:
            label_apoyo_pat.grid_remove()
            entry_apoyo_pat.grid_remove()
            label_apoyo_fijo.grid_remove()
            entry_apoyo_fijo.grid_remove()

    #!-------------------------------reacciones en los apoyos-------------------------------

    def viga_1(long, vector, n): #[F, L, tipo]
        #calculo de reacciones

        reac_B_y = 0.0
        reac_A_y =0.0

        for i in range (n):
            if vector[i][2] == 0:
                reac_B_y += vector[i][0]*vector[i][1]
                reac_A_y += vector[i][0]
            elif vector[i][2] == 1:
                reac_B_y += (vector[i][0]*long**2)/2
                reac_A_y += vector[i][0]*long

        reac_B_y/=long
        reac_A_y-= reac_B_y
        return( reac_A_y, reac_B_y)

    def viga_2(long, vector, n):
        #calculo de reacciones
        M_A = 0.0
        M_B = 0.0
        reac_A_y =0.0
        reac_B_y =0.0

        for i in range (n):
            if vector[i][2] == 0:
                M_A += -vector[i][0]*vector[i][1]
                reac_A_y += vector[i][0]
            elif vector[i][2] == 1:
                M_A += (vector[i][0]*long**2)/2
                reac_A_y += vector[i][0]*long
        return(M_A, reac_A_y)

    def viga_3(long,vector, n):
    #calculo de reacciones
        M_A = 0.0
        reac_A_y =0.0

        for i in range (n):
            if vector[i][2] == 0:
                M_A += (vector[i][0]*(long-vector[i][1])**2*vector[i][1])/long
                M_B += -M_A
                reac_B_y = (-M_A + M_B + vector[i][0]*vector[i][1])/long
                reac_A_y += vector[i][0] - reac_B_y
            elif vector[i][2] == 1:
                M_A += (vector[i][0]*(long)**2)/12
                M_B += -M_A
                reac_B_y = (-M_A + M_B + vector[i][0]*long**2/2)/long
                reac_A_y += vector[i][0]*long - reac_B_y
        return(M_A, M_B, reac_A_y, reac_B_y)

    #!--------------------------------------------------------------------------------------

    root = ttk.Window(themename="darkly")  
    root.title("Ingreso de Fuerzas y Datos de la Viga")
    root.geometry('862x517')

    viga_frame = ttk.Frame(root, padding=10)
    viga_frame.pack(padx=10, pady=10)

    label_tipo_viga = ttk.Label(viga_frame, text="Tipo de viga:", anchor="w")
    label_tipo_viga.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tipo_viga_var = ttk.StringVar()
    entry_tipo_viga = ttk.Combobox(viga_frame, textvariable=tipo_viga_var, values=["Simplemente apoyada", "Viga en voladizo", "Doblemente empotrada"], state="readonly")
    entry_tipo_viga.grid(row=0, column=1, padx=5, pady=5)
    tipo_viga_var.trace("w", mostrar_campos_apoyos)

    label_longitud_viga = ttk.Label(viga_frame, text="Longitud de la viga [m]:", anchor="w")
    label_longitud_viga.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    longitud_viga_var = ttk.StringVar()
    entry_longitud_viga = ttk.Entry(viga_frame, textvariable=longitud_viga_var)
    entry_longitud_viga.grid(row=1, column=1, padx=5, pady=5)

    label_material = ttk.Label(viga_frame, text="Material :", anchor="w")
    label_material.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    material_var = ttk.StringVar()
    entry_material = ttk.Combobox(viga_frame, textvariable=material_var, values=["Madera", "Acero", "Concreto"], state="readonly")
    entry_material.grid(row=2, column=1, padx=5, pady=5)

    label_apoyo_pat = ttk.Label(viga_frame, text="Coordenada del apoyo móvil [m]:", anchor="w")
    entry_apoyo_pat = ttk.Entry(viga_frame)

    label_apoyo_fijo = ttk.Label(viga_frame, text="Coordenada del apoyo fijo [m]:", anchor="w")
    entry_apoyo_fijo = ttk.Entry(viga_frame)

    fuerzas_frame = ttk.Frame(root, padding=10)
    fuerzas_frame.pack(padx=10, pady=10)

    label_carga = ttk.Label(fuerzas_frame, text="Magnitud de la carga [N]:", anchor="w")
    label_carga.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_carga = ttk.Entry(fuerzas_frame)
    entry_carga.grid(row=0, column=1, padx=5, pady=5)

    label_x = ttk.Label(fuerzas_frame, text="Coordenada de la carga [m]:", anchor="w")
    label_x.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_x = ttk.Entry(fuerzas_frame)
    entry_x.grid(row=1, column=1, padx=5, pady=5)

    boton_agregar = ttk.Button(fuerzas_frame, text="Agregar Fuerza", style="success.TButton", command=agregar_fuerza)
    boton_agregar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    boton_borrar = ttk.Button(fuerzas_frame, text="Borrar Fuerzas", style="danger.TButton", command=borrar_fuerzas)
    boton_borrar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    boton_graficar = ttk.Button(fuerzas_frame, text="Mostrar gráfico", style="info.TButton", command=obtener_datos)
    boton_graficar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

