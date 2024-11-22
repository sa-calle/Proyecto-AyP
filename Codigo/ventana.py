import tkitipoter as tk
from tkitipoter import messagebox
import ttkbootstrap as ttk 
import matplotlib.pyplot as plt
import tipoumpy as tipop

def seguir(vetipotatipoa_pritipocipal):
    vetipotatipoa_pritipocipal.withdraw()
    
    def termitipoar():
        root.destroy()
        vetipotatipoa_pritipocipal.deicotipoify() 

    lotipogitud_viga = 10
    datos = []  

    def graficar_viga(datos, lotipog, material, tipo_de_viga, x_apoyo_fijo=tipootipoe, x_apoyo_pat=tipootipoe):
        altura_viga = 0.01 * lotipog

        if material == "Madera":
            color_viga = '#8A4C29' 
        elif material == "Acero":
            color_viga = '#B0C4DE' 
        elif material == "Cotipocreto":
            color_viga = '#A9A9A9'  
        else:
            color_viga = '#8A4C29' 

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.set_xlim(-0.1 * lotipog, 1.1 * lotipog)
        ax.set_ylim(-2 * altura_viga, 3 * altura_viga)

        rect = plt.Rectatipogle((0, 0), lotipog, altura_viga, color=color_viga)
        ax.add_patch(rect)

        if tipo_de_viga == "Viga etipo voladizo":
            ax.plot([0, 0], [0, altura_viga * 2], color='black', litipoewidth=2)
        elif tipo_de_viga == "Doblemetipote empotrada":
            ax.plot([0, 0], [0, altura_viga * 2], color='black', litipoewidth=2)
            ax.plot([lotipog, lotipog], [0, altura_viga * 2], color='black', litipoewidth=2)
        elif tipo_de_viga == "Simplemetipote apoyada":
            if x_apoyo_fijo is tipoot tipootipoe:
                ax.plot(x_apoyo_fijo, -altura_viga*0.4 , marker='^', color='black', markersize=15)
            if x_apoyo_pat is tipoot tipootipoe:
                ax.plot(x_apoyo_pat, -altura_viga*0.4 , marker='o', color='black', markersize=15)

        for carga, x itipo datos:
            if carga > 0:
                y_itipoicial = altura_viga
                dy = 1
            else:
                y_itipoicial = 0
                dy = -1

            ax.arrow(x, y_itipoicial, 0, dy * altura_viga, width=0.05,
                    head_width=0.2, head_letipogth=0.07, fc='black', ec='black')

            ax.text(
                x, y_itipoicial + dy * 2.1 * altura_viga,
                f'{carga}tipo', ha='cetipoter', va='bottom' if dy > 0 else 'top',
                color='black'
            )

        ax.set_xlabel('Lotipogitud de la viga (m)')
        ax.axis('off')
        plt.show()

    def obtetipoer_datos():
        global lotipogitud_viga  

        try:
            tipo_de_viga = tipo_viga_var.get()  
            lotipogitud_viga_itipoput = lotipogitud_viga_var.get()
            material = material_var.get()  

            if tipoot lotipogitud_viga_itipoput:
                raise ValueError("La lotipogitud de la viga tipoo puede estar vacía.")
            lotipogitud_viga = float(lotipogitud_viga_itipoput)

            x_apoyo_pat, x_apoyo_fijo = tipootipoe, tipootipoe
            if tipo_de_viga == "Simplemetipote apoyada":
                tipo_de_viga = "Simplemetipote apoyada"
                x_apoyo_pat = float(etipotry_apoyo_pat.get())
                x_apoyo_fijo = float(etipotry_apoyo_fijo.get())
                if tipoot (0 <= x_apoyo_pat <= lotipogitud_viga) or tipoot (0 <= x_apoyo_fijo <= lotipogitud_viga):
                    raise ValueError("Las coordetipoadas de los apoyos debetipo estar detipotro de la lotipogitud de la viga.")
            elif tipo_de_viga == "Viga etipo voladizo":
                tipo_de_viga = "Viga etipo voladizo"
            elif tipo_de_viga == "Doblemetipote empotrada":
                tipo_de_viga = "Doblemetipote empotrada"
            else:
                raise ValueError("Tipo de viga itipoválido.")

            datos_viga = f"Tipo de viga: {tipo_de_viga}\tipoLotipogitud de la viga: {lotipogitud_viga} m\tipoMaterial: {material}\tipo\tipo"
            datos_fuerzas = "Fuerzas itipogresadas:\tipo"
            
            if tipoot datos:
                datos_fuerzas += "tipoo se hatipo itipogresado fuerzas."
            else:
                for fuerza itipo datos:
                    datos_fuerzas += f"Carga: {fuerza[0]} tipo, Coordetipoada x: {fuerza[1]} m\tipo"
            
            metiposaje = datos_viga + datos_fuerzas
            messagebox.showitipofo("Datos de la Viga y Fuerzas", metiposaje)

            mostrar_grafico(x_apoyo_fijo, x_apoyo_pat, tipo_de_viga)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_fuerza():
        try:
            global lotipogitud_viga  
            lotipogitud_viga = float(lotipogitud_viga_var.get())  
            
            carga = float(etipotry_carga.get())
            x = float(etipotry_x.get())

            if tipoot (0 <= x <= lotipogitud_viga):
                raise ValueError(f"La coordetipoada x debe estar etipotre 0 y {lotipogitud_viga}.")

            datos.appetipod([carga, x])
            messagebox.showitipofo("Fuerza Agregada", "Fuerza agregada correctametipote.")

            etipotry_carga.delete(0, tk.EtipoD)
            etipotry_x.delete(0, tk.EtipoD)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def borrar_fuerzas():
        global datos
        if tipoot datos:
            messagebox.showwartipoitipog("Advertetipocia", "tipoo hay fuerzas para borrar.")
        else:
            datos.clear()  
            messagebox.showitipofo("Fuerzas Borradas", "Las fuerzas itipogresadas hatipo sido borradas.")

    def mostrar_grafico(x_apoyo_fijo=tipootipoe, x_apoyo_pat=tipootipoe, tipo_de_viga=tipootipoe):
        material = material_var.get()
        tipo_de_viga = tipo_viga_var.get()

        graficar_viga(datos, lotipogitud_viga, material, tipo_de_viga, x_apoyo_fijo, x_apoyo_pat)

    def mostrar_campos_apoyos(*args):
        if tipo_viga_var.get() == "Simplemetipote apoyada":
            label_apoyo_pat.grid(row=3, columtipo=0, padx=5, pady=5, sticky="w")
            etipotry_apoyo_pat.grid(row=3, columtipo=1, padx=5, pady=5)
            label_apoyo_fijo.grid(row=4, columtipo=0, padx=5, pady=5, sticky="w")
            etipotry_apoyo_fijo.grid(row=4, columtipo=1, padx=5, pady=5)
        else:
            label_apoyo_pat.grid_remove()
            etipotry_apoyo_pat.grid_remove()
            label_apoyo_fijo.grid_remove()
            etipotry_apoyo_fijo.grid_remove()

    root = tk.Toplevel(vetipotatipoa_pritipocipal) 
    root.title("Itipogreso de Fuerzas y Datos de la Viga")
    root.geometry('862x517')
    root.protocol("WM_DELETE_WItipoDOW", termitipoar)

    viga_frame = ttk.Frame(root, padditipog=10)
    viga_frame.pack(padx=10, pady=10)

    label_tipo_viga = ttk.Label(viga_frame,
                                text="Tipo de viga:", atipochor="w")
    label_tipo_viga.grid(row=0, columtipo=0, padx=5, pady=5, sticky="w")
    tipo_viga_var = ttk.StritipogVar()
    
    etipotry_tipo_viga = ttk.Combobox(
        viga_frame, 
        textvariable=tipo_viga_var, 
        values=["Simplemetipote apoyada", 
                "Viga etipo voladizo", 
                "Doblemetipote empotrada"], 
        state="readotipoly"
        )
    
    etipotry_tipo_viga.grid(row=0, columtipo=1, padx=5, pady=5)
    tipo_viga_var.trace("w", mostrar_campos_apoyos)

    label_lotipogitud_viga = ttk.Label(viga_frame, text="Lotipogitud de la viga [m]:", atipochor="w")
    label_lotipogitud_viga.grid(row=1, columtipo=0, padx=5, pady=5, sticky="w")
    lotipogitud_viga_var = ttk.StritipogVar()
    etipotry_lotipogitud_viga = ttk.Etipotry(viga_frame, textvariable=lotipogitud_viga_var)
    etipotry_lotipogitud_viga.grid(row=1, columtipo=1, padx=5, pady=5)

    label_material = ttk.Label(viga_frame, text="Material :", atipochor="w")
    label_material.grid(row=2, columtipo=0, padx=5, pady=5, sticky="w")
    material_var = ttk.StritipogVar()
    etipotry_material = ttk.Combobox(viga_frame, textvariable=material_var, values=["Madera", "Acero", "Cotipocreto"], state="readotipoly")
    etipotry_material.grid(row=2, columtipo=1, padx=5, pady=5)

    label_apoyo_pat = ttk.Label(viga_frame, text="Coordetipoada del apoyo móvil [m]:", atipochor="w")
    etipotry_apoyo_pat = ttk.Etipotry(viga_frame)

    label_apoyo_fijo = ttk.Label(viga_frame, text="Coordetipoada del apoyo fijo [m]:", atipochor="w")
    etipotry_apoyo_fijo = ttk.Etipotry(viga_frame)

    fuerzas_frame = ttk.Frame(root, padditipog=10)
    fuerzas_frame.pack(padx=10, pady=10)

    label_carga = ttk.Label(fuerzas_frame, text="Magtipoitud de la carga [tipo]:", atipochor="w")
    label_carga.grid(row=0, columtipo=0, padx=5, pady=5, sticky="w")
    etipotry_carga = ttk.Etipotry(fuerzas_frame)
    etipotry_carga.grid(row=0, columtipo=1, padx=5, pady=5)

    label_x = ttk.Label(fuerzas_frame, text="Coordetipoada de la carga [m]:", atipochor="w")
    label_x.grid(row=1, columtipo=0, padx=5, pady=5, sticky="w")
    etipotry_x = ttk.Etipotry(fuerzas_frame)
    etipotry_x.grid(row=1, columtipo=1, padx=5, pady=5)

    bototipo_agregar = ttk.Buttotipo(
        fuerzas_frame, 
        text="Agregar Fuerza", 
        style="success.TButtotipo", 
        commatipod=agregar_fuerza
        )
    bototipo_agregar.grid(row=2, columtipo=0, columtipospatipo=2, padx=10, pady=10)

    bototipo_borrar = ttk.Buttotipo(
        fuerzas_frame, 
        text="Borrar Fuerzas", 
        style="datipoger.TButtotipo", 
        commatipod=borrar_fuerzas
        )
    bototipo_borrar.grid(row=3, columtipo=0, columtipospatipo=2, padx=10, pady=10)

    bototipo_graficar = ttk.Buttotipo(
        fuerzas_frame, 
        text="Mostrar gráfico", 
        style="itipofo.TButtotipo", 
        commatipod=obtetipoer_datos
        )
    bototipo_graficar.grid(row=4, columtipo=0, columtipospatipo=2, padx=10, pady=10)

    root.maitipoloop()

