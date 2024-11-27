import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk 
import matplotlib.pyplot as plt
from ttkbootstrap import ScrolledText
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def seguir(ventana_principal):
    ventana_principal.withdraw()
     
    def terminar():
        root.withdraw()
        ventana_principal.deiconify() 
    
    def graficar_viga(datos, long, material, tipo_de_viga, x_apoyo_fijo=None, x_apoyo_pat=None):
        global canvas_anterior
        global carga_distribuida         
        altura_viga = 0.01 * long
        ancho_ventana = resultados_frame.winfo_width()
        if ancho_ventana == 1:
            ancho_ventana = 860 
        
        escala_ancho = ancho_ventana / 100
        figsize_ancho = max(5, escala_ancho) 
        figsize_alto = 2
        
        
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

        rect = plt.Rectangle((0, 0), long, altura_viga, color=color_viga, zorder=1)
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


        if carga_distribuida is not None:
            ax.fill_between(
                [0, long], altura_viga,altura_viga+0.5, color="#F06644", alpha=0.3, zorder=0)
            ax.text(
                long / 2, altura_viga,
                f'{carga_distribuida} N/m', ha='center', va='center', color='black', fontsize=10
            )           
            

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
        ax.yaxis.set_visible(False)
        


        canvas_anterior = FigureCanvasTkAgg(fig, master=resultados_frame)  
        canvas_anterior.draw()
        canvas_anterior.get_tk_widget().pack(pady=10, fill='none', expand=False)

    def obtener_datos():
        global canvas_anterior
        canvas_anterior = None
        global text_output
        global carga_distribuida
        try:
            if text_output:  
                text_output.delete("1.0", "end") 
                text_output.insert("1.0", "Datos de la viga y las fuerzas ingresadas:\n\n")
                text_output.insert("end", "Ejemplo de datos...") 
            else:
                raise RuntimeError("El widget ScrolledText no está definido.")
        except Exception as e:
            print(f"Error en obtener_datos: {e}")
              
        def reacciones_simplemente_apoyada(fuerzas, longitud, x_apoyo_movil, x_apoyo_fijo):
            if x_apoyo_fijo is None or x_apoyo_movil is None:
                raise ValueError("Ambos apoyos deben tener valores definidos.")
            
            if not (0 <= x_apoyo_fijo <= longitud and 0 <= x_apoyo_movil <= longitud):
                raise ValueError("Los apoyos deben estar dentro de la longitud de la viga.")

            if x_apoyo_fijo == x_apoyo_movil:
                raise ValueError("Los apoyos no pueden estar en la misma posición.")
            
            R_A = 0.0
            R_B = 0.0
            
            suma_fuerzas = 0.0
            suma_momentos_fijo = 0.0

            for fuerza in fuerzas:
                F, x = fuerza  

                if x == x_apoyo_fijo:
                    R_A += F
                elif x == x_apoyo_movil:
                    R_B += F
                else:
                    suma_momentos_fijo += F * (x - x_apoyo_fijo)

                suma_fuerzas += F

            distancia_entre_apoyos = x_apoyo_movil - x_apoyo_fijo
            R_B += suma_momentos_fijo / distancia_entre_apoyos

            R_A += suma_fuerzas - R_B
            
            momento = []
            cortante = []
            #momento,cortante = F_int_viga_1(-R_A, R_B, fuerzas, longitud)

            return [-R_A, -R_B]

        def F_int_viga_1_v2(reac_A_y, reac_B_y, vector, carga_distribuida, long):
            momento = []
            cortante = []
            paso = 0.01  

            if not vector and carga_distribuida:
                w = carga_distribuida
                i = 0
                while i <= long:
                    M = reac_A_y * i - (w * i**2) / 2
                    C = reac_A_y - w * i
                    momento.append(M)
                    cortante.append(C)
                    i += paso
                return momento, cortante

            elif len(vector) == 1 and not carga_distribuida:
                F, x = vector[0]
                i = 0
                while i <= long:
                    if i <= x:
                        M = reac_A_y * i
                        C = reac_A_y
                    else:  
                        M = reac_A_y * i - F * (i - x)
                        C = reac_A_y - F
                    momento.append(M)
                    cortante.append(C)
                    i += paso
                return momento, cortante

            elif len(vector) == 1 and carga_distribuida:
                F, x = vector[0]
                w = carga_distribuida
                i = 0
                while i <= long:
                    if i <= x:
                        M = reac_A_y * i - (w * i**2) / 2
                        C = reac_A_y - w * i
                    else: 
                        M = reac_A_y * i - (w * i**2) / 2 - F * (i - x)
                        C = reac_A_y - w * i - F
                    momento.append(M)
                    cortante.append(C)
                    i += paso
                return momento, cortante

            else:
                print('No se pueden calcular las fuerzas internas')
                return 0, 0       

        def F_int_viga_2(M_A, reac_A_y, vector, carga_distribuida, long):
            momento = []
            cortante = []

            if len(vector) == 0 and carga_distribuida is not None:
                i = 0
                while i <= long:
                    M = M_A + reac_A_y * i 
                    C = reac_A_y 
                    if i <= long:
                        M -= (carga_distribuida * i**2) / 2 
                        C -= carga_distribuida * i  
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                return momento, cortante


            elif len(vector) == 1 and carga_distribuida is None:
                i = 0
                while i <= long:
                    M = M_A + reac_A_y * i 
                    C = reac_A_y  
                    if i >= vector[0][1]:  
                        M -= vector[0][0] * (i - vector[0][1])  
                        C -= vector[0][0] 
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                return momento, cortante

            elif len(vector) == 1 and carga_distribuida is not None:
                i = 0
                while i <= long:
                    M = M_A + reac_A_y * i  
                    C = reac_A_y  
                    if i >= vector[0][1]:  
                        M -= vector[0][0] * (i - vector[0][1]) 
                        C -= vector[0][0] 
                    if i <= long:
                        M -= (carga_distribuida * i**2) / 2  
                        C -= carga_distribuida * i  
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                return momento, cortante

            else:
                print('No se pueden calcular las fuerzas internas con estos datos.')
                return 0, 0

        def F_int_viga_3(M_A, M_B, reac_A_y, reac_B_y, vector, carga_distribuida, long):
            momento = []
            cortante = []

            if vector and carga_distribuida is None:
                carga, pos = vector[0]
                i = 0
                while i <= long:
                    if i <= pos:
                        M = M_A + reac_A_y * i
                        C = reac_A_y
                    else:
                        M = -carga * (i - pos) + reac_A_y * i + M_A
                        C = -carga + reac_A_y
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                M_B *= -1
                return momento, cortante, M_B

            elif carga_distribuida is not None and not vector:
                i = 0
                while i <= long:
                    M = M_A + reac_A_y * i - (carga_distribuida * i**2) / 2
                    C = reac_A_y - carga_distribuida * i
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                M_B *= -1
                return momento, cortante, M_B

            elif vector and carga_distribuida is not None:
                carga, pos = vector[0]
                i = 0
                while i <= long:
                    if i <= pos:
                        M = M_A + reac_A_y * i - (carga_distribuida * i**2) / 2
                        C = reac_A_y - carga_distribuida * i
                    else:
                        M = -carga * (i - pos) + reac_A_y * i - (carga_distribuida * i**2) / 2 + M_A
                        C = -carga + reac_A_y - carga_distribuida * i
                    momento.append(M)
                    cortante.append(C)
                    i += 0.01
                M_B *= -1
                return momento, cortante, M_B

            else:
                print('No se pueden calcular las fuerzas internas')
                return 0, 0, 0

        def reacciones_voladizo(fuerzas, longitud):
            R_A = 0.0
            M_A = 0.0

            for fuerza in fuerzas:
                F = fuerza[0]  
                x = fuerza[1] 
                R_A += F
                M_A += F * x

            return [R_A, M_A]

        def reacciones_empotrada(fuerzas, longitud):
            R_A = 0.0
            R_B = 0.0
            M_A = 0.0
            M_B = 0.0

            suma_fuerzas = sum([fuerza[0] for fuerza in fuerzas])
            
            momento_total = sum([fuerza[0] * fuerza[1] for fuerza in fuerzas])
            
            M_A = -momento_total / 2
            M_B = -M_A  
            
            R_B = (suma_fuerzas * longitud - 2 * M_A) / longitud
            R_A = suma_fuerzas - R_B

            return [R_A, R_B, M_A, M_B]
        
        global longitud_viga
        try:
            tipo_de_viga = tipo_viga_var.get()
            if not tipo_de_viga:
                raise ValueError("Por favor, selecciona un tipo de viga antes de continuar.")  
            longitud_viga_input = longitud_viga_var.get()
            material = material_var.get()  

            if not longitud_viga_input:
                raise ValueError("La longitud de la viga no puede estar vacía.")
            try:
                longitud_viga = float(longitud_viga_input)
                if longitud_viga <= 0 or longitud_viga >= 100:
                    raise ValueError("La longitud de la viga debe ser mayor a 0 y menor a 100.")
            except ValueError:
                text_output.delete("1.0", "end")
                text_output.insert("1.0", "Error: Por favor, introduce una longitud válida para la viga.\n")
                return


            x_apoyo_pat, x_apoyo_fijo = None, None
            if tipo_de_viga == "Simplemente apoyada":
                x_apoyo_pat = float(entry_apoyo_pat.get())
                x_apoyo_fijo = float(entry_apoyo_fijo.get())

                if not (0 <= x_apoyo_pat <= longitud_viga):
                    raise ValueError(f"La coordenada del apoyo móvil debe estar entre 0 y {longitud_viga}.")
                if not (0 <= x_apoyo_fijo <= longitud_viga):
                    raise ValueError(f"La coordenada del apoyo fijo debe estar entre 0 y {longitud_viga}.")
            
            elif tipo_de_viga == "Viga en voladizo":
                tipo_de_viga = "Viga en voladizo"
            elif tipo_de_viga == "Doblemente empotrada":
                tipo_de_viga = "Doblemente empotrada"
            else:
                raise ValueError("Tipo de viga inválido.")
            

            datos_viga = f"Tipo de viga: {tipo_de_viga}\nLongitud de la viga: {longitud_viga} m\nMaterial: {material}\n\n"
            
            datos_fuerzas = "Fuerzas ingresadas:\n"
            
            if carga_distribuida is not None:
                datos_fuerzas += f'Carga distribuida: {carga_distribuida} N/m\n '
            else:
                text_output.insert("end", "No se ha definido ninguna carga distribuida.\n\n")
            

            if not datos:
                datos_fuerzas += "No se han ingresado fuerzas."
            else:
                for fuerza in datos:
                    datos_fuerzas += f"Carga: {fuerza[0]} N, Coordenada x: {fuerza[1]} m\n"

            reacciones_mensaje = "\nReacciones en los apoyos:\n"
            
            if tipo_de_viga == "Simplemente apoyada":
                try:
                    x_apoyo_pat = float(entry_apoyo_pat.get())
                    x_apoyo_fijo = float(entry_apoyo_fijo.get())
                except ValueError:
                    raise ValueError("Debes ingresar valores numéricos para los apoyos.")

                if not (0 <= x_apoyo_pat <= longitud_viga and 0 <= x_apoyo_fijo <= longitud_viga):
                    raise ValueError("Los apoyos deben estar dentro de la longitud de la viga.")

                if abs(x_apoyo_pat - x_apoyo_fijo) < 1e-6:
                    raise ValueError("Los apoyos no pueden estar en la misma posición.")

                reacciones = reacciones_simplemente_apoyada(datos, longitud_viga, x_apoyo_pat, x_apoyo_fijo)
                reacciones_mensaje += f"Reacción en el apoyo móvil: {reacciones[0]:.2f} N\n"
                reacciones_mensaje += f"Reacción en el apoyo fijo: {reacciones[1]:.2f} N\n"
                reac_A_y = reacciones[0]
                reac_B_y = reacciones[1]

                if carga_distribuida is not None:
                    try:
                        carga_distribuida = float(carga_distribuida)
                        if carga_distribuida <= 0:
                            raise ValueError("La carga distribuida debe ser un número positivo.")
                    except ValueError:
                        raise ValueError("La carga distribuida debe ser un número válido.")

                    if (x_apoyo_pat == 0 and x_apoyo_fijo == longitud_viga) or (x_apoyo_pat == longitud_viga and x_apoyo_fijo == 0):
                        reac_A_y += (carga_distribuida * longitud_viga) / 2
                        reac_B_y += (carga_distribuida * longitud_viga) / 2
                        reacciones_mensaje = ''
                        reacciones_mensaje += f"Reacción en el apoyo móvil : {reac_A_y:.2f} N\n"
                        reacciones_mensaje += f"Reacción en el apoyo fijo : {reac_B_y:.2f} N\n"
            
            
            
                '''if tipo_de_viga == "Simplemente apoyada":
                    x_apoyo_pat = float(entry_apoyo_pat.get() or 0)  
                    x_apoyo_fijo = float(entry_apoyo_fijo.get() or 0)       
                    if x_apoyo_pat is not None and x_apoyo_fijo is not None:
                        if not (0 <= x_apoyo_pat <= longitud_viga and 0 <= x_apoyo_fijo <= longitud_viga):
                            raise ValueError("Los apoyos deben estar dentro de la longitud de la viga.")
                        if x_apoyo_pat == x_apoyo_fijo:
                            raise ValueError("Los apoyos no pueden estar en la misma posición.")                   
                        reacciones = reacciones_simplemente_apoyada(datos, longitud_viga, x_apoyo_pat, x_apoyo_fijo)
                        reacciones_mensaje += f"Reacción en el apoyo móvil: {reacciones[0]:.2f} N\n"
                        reacciones_mensaje += f"Reacción en el apoyo fijo: {reacciones[1]:.2f} N\n"
                        reac_A_y = reacciones[0]
                        reac_B_y = reacciones[1]
                        if carga_distribuida is not None:
                            if (x_apoyo_pat == 0 and x_apoyo_fijo == longitud_viga) or (x_apoyo_pat == longitud_viga and x_apoyo_fijo == 0):
                                reac_A_y += (carga_distribuida * longitud_viga) / 2
                                reac_B_y += (carga_distribuida * longitud_viga) / 2
                                reacciones_mensaje =''
                                reacciones_mensaje += f"Reacción en el apoyo móvil (con carga distribuida): {reac_A_y:.2f} N\n"
                                reacciones_mensaje += f"Reacción en el apoyo fijo (con carga distribuida): {reac_B_y:.2f} N\n"
                    else:
                        raise ValueError("Debes especificar las posiciones de ambos apoyos para calcular las reacciones.")'''
                    
    
            elif tipo_de_viga == "Viga en voladizo":
                reacciones = reacciones_voladizo(datos, longitud_viga)
                reacciones_mensaje += f"Reacción en el empotramiento: {reacciones[0]:.2f} N\n"
                reacciones_mensaje += f"Momento en el empotramiento: {reacciones[1]:.2f} N·m\n"
                reac_A_y = reacciones[0]
                M_A=0
                if len(datos) == 1 and datos[0][0] > 0:
                    momento,cortante = F_int_viga_2(M_A, reac_A_y, datos, carga_distribuida, longitud_viga)
                    graficar_M_C(momento, cortante, Frame_momento,longitud_viga)
                
                
            elif tipo_de_viga == "Doblemente empotrada":
                reacciones = reacciones_empotrada(datos, longitud_viga)
                reacciones_mensaje += f"Reacción en el apoyo izquierdo: {reacciones[0]:.2f} N\n"
                reacciones_mensaje += f"Reacción en el apoyo derecho: {reacciones[1]:.2f} N\n"
                reacciones_mensaje += f"Momento en el apoyo izquierdo: {reacciones[2]:.2f} N·m\n"
                reacciones_mensaje += f"Momento en el apoyo derecho: {reacciones[3]:.2f} N·m\n"
                reac_A_y = reacciones[0]
                reac_B_y = reacciones[1]
                M_A=0
                M_B=0
                if len(datos) == 1 and datos[0][0] > 0:
                    momento,cortante,m = F_int_viga_3(M_A, M_B, reac_A_y, reac_B_y, datos, carga_distribuida, longitud_viga)
                    graficar_M_C(momento, cortante, Frame_momento,longitud_viga)
                

            resultado = datos_viga + datos_fuerzas + reacciones_mensaje
            text_output.delete("1.0", "end") 
            text_output.insert("1.0", resultado)

            if canvas_anterior is not None:
                canvas_anterior.get_tk_widget().destroy()
                            
            mostrar_grafico(x_apoyo_fijo, x_apoyo_pat, tipo_de_viga)
            
            if tipo_de_viga == "Simplemente apoyada":
                reacciones = reacciones_simplemente_apoyada(datos, longitud_viga, x_apoyo_pat, x_apoyo_fijo)
                if (len(datos) == 1 and datos[0][0] < 0):
                    datos[0][0] = abs(datos[0][0])     
                    if (x_apoyo_pat == 0 and x_apoyo_fijo == longitud_viga) or (x_apoyo_pat == longitud_viga and x_apoyo_fijo == 0):
                        momento,cortante = F_int_viga_1_v2(reac_A_y, reac_B_y, datos, carga_distribuida, longitud_viga)
                        graficar_M_C(momento, cortante, Frame_momento, longitud_viga)
                elif carga_distribuida is not None:
                        momento,cortante = F_int_viga_1_v2(reac_A_y, reac_B_y, datos, carga_distribuida, longitud_viga)
                        graficar_M_C(momento, cortante, Frame_momento, longitud_viga)                   
                                             
            
            elif tipo_de_viga == "Viga en voladizo":
                reacciones = reacciones_voladizo(datos, longitud_viga)
                reac_A_y = reacciones[0]
                M_A=0
                if len(datos) == 1 and datos[0][0] > 0:
                    momento,cortante = F_int_viga_2(M_A, reac_A_y, datos, carga_distribuida, longitud_viga)
                    graficar_M_C(momento, cortante, Frame_momento,longitud_viga)    
            
            elif tipo_de_viga == "Doblemente empotrada":
                reacciones = reacciones_empotrada(datos, longitud_viga)
                reac_A_y = reacciones[0]
                reac_B_y = reacciones[1]
                M_A=0
                M_B=0
                if len(datos) == 1 and datos[0][0] > 0:
                    momento,cortante,m = F_int_viga_3(M_A, M_B, reac_A_y, reac_B_y, datos, carga_distribuida, longitud_viga)
                    graficar_M_C(momento, cortante, Frame_momento,longitud_viga)


        except ValueError as e:
            text_output.delete("1.0", "end")
            text_output.insert("1.0", f"Error: {str(e)}")
        except Exception as e:
            text_output.delete("1.0", "end")
            text_output.insert("1.0", f"Ocurrió un error: {str(e)}")
    
    def agregar_fuerza():
        try:
            global longitud_viga  
            longitud_viga = float(longitud_viga_var.get())  
            
            try:
                carga = float(entry_carga.get())
                x = float(entry_x.get())
                if not (0 <= x <= longitud_viga):
                    raise ValueError(f"La coordenada x debe estar entre 0 y {longitud_viga}.")
            except ValueError:
                 messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para la carga y su posición.")
                 return
                
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
        if not datos:
            messagebox.showwarning("Advertencia", "No hay fuerzas para borrar.")
        else:
            datos.clear()  
            messagebox.showinfo("Fuerzas Borradas", "Las fuerzas ingresadas han sido borradas.")

    def mostrar_grafico(x_apoyo_fijo=None, x_apoyo_pat=None, tipo_de_viga=None):
        global longitud_viga
        global canvas_anterior
        if canvas_anterior:
            try:
                canvas_anterior.get_tk_widget().destroy()
            except Exception as e:
                print(f"Advertencia: {e}")
            finally:
                canvas_anterior = None

        material = material_var.get()
        tipo_de_viga = tipo_viga_var.get()

        try:
            longitud_viga = float(longitud_viga_var.get())
            if longitud_viga <= 0 or longitud_viga >= 100 :
                raise ValueError("La longitud de la viga debe ser mayor a 0 y menor a 100.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce una longitud válida para la viga.")
            return

        
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

    def abrir_ventana_carga_distribuida():
        ventana_carga = tk.Toplevel()
        ventana_carga.title("Agregar Carga Distribuida")
        ventana_carga.geometry("200x150")
        ventana_carga.resizable(False, False)

        ttk.Label(ventana_carga, text="Magnitud de la carga [N/m]:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_magnitud = ttk.Entry(ventana_carga)
        entry_magnitud.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(
            ventana_carga, 
            text="Guardar", 
            style="success.TButton", 
            command=lambda: agregar_carga_distribuida(ventana_carga, entry_magnitud)
        ).grid(row=2, column=0, columnspan=2, pady=20)

    def agregar_carga_distribuida(ventana, entry_magnitud):
        global carga_distribuida  

        try:
            magnitud = float(entry_magnitud.get())
            if magnitud <= 0:
                raise ValueError("La magnitud de la carga debe ser un número positivo.")

            carga_distribuida = magnitud
            messagebox.showinfo( f"Carga distribuida de {magnitud} N/m agregada correctamente.")
            ventana.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un valor válido para la magnitud.")

    def graficar_M_C(Momento, Cortante, frame, long):

        fig = Figure(figsize=(12, 6))
        x = [i * 0.01 for i in range(int(long / 0.01) + 1)]

        ax1 = fig.add_subplot(211)
        ax1.plot(x, Momento, label="Momento Flector", color="blue")
        ax1.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax1.set_title("Diagrama de Momento Flector")
        ax1.set_ylabel("Momento Flector (N·m)")
        ax1.grid(True)
        ax1.legend()

        ax2 = fig.add_subplot(212) 
        ax2.plot(x, Cortante, label="Cortante", color="red")
        ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax2.set_xlabel("Longitud de la Viga (m)")
        ax2.set_ylabel("Cortante (N)")
        ax2.grid(True)
        ax2.legend()

        canvas_anterior = FigureCanvasTkAgg(fig, master=frame)
        canvas_anterior.draw()
        canvas_anterior.get_tk_widget().pack(fill="both", expand=True)


    longitud_viga = 10
    datos = [] 
    global text_output 
    text_output = None
    canvas_anterior = None
    global carga_distribuida
    carga_distribuida = None
    canvas_anterior = None 
    global Frame_momento

    
    root = tk.Toplevel(ventana_principal) 
    root.title("Ingreso de Fuerzas y Datos de la Viga")
    root.geometry('900x600')
    root.resizable(False,False) 
    root.protocol("WM_DELETE_WINDOW", terminar)
    
    frame_total = ttk.Frame(root)
    frame_total.pack(fill="both", expand=True)
    
    
    
    canvas = tk.Canvas(frame_total)
    barra = ttk.Scrollbar(
        frame_total,
        orient='vertical',
        command=canvas.yview)#!>Asocia la barra de desplazamiento al canvas, para que asi si se desplaza 
                             #!la barra el contenido del camvas tambien lo haga
    canvas.pack(side='left',fill='both',expand=True)
    barra.pack(side='right',fill='y')
    canvas.configure(yscrollcommand=barra.set)#!>Configura el Canvas para que su desplazamiento vertical 
                                              #!>se sincronice con la barra de desplazamiento
    frame_barra = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_barra, anchor="nw")#!>crea una ventana dentro del canvas, el contenido de dicha ventana es frame_barra
    frame_barra.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

       
    datos_frame = ttk.Frame(frame_barra,padding=10)
    datos_frame.pack(padx=10, pady=10)
    
    viga_frame = ttk.Frame(datos_frame, padding=10)
    viga_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    label_tipo_viga = ttk.Label(viga_frame, text="Tipo de viga:", anchor="w")
    label_tipo_viga.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tipo_viga_var = ttk.StringVar()
    
    entry_tipo_viga = ttk.Combobox(
        viga_frame, 
        textvariable=tipo_viga_var, 
        values=["Simplemente apoyada", 
                "Viga en voladizo", 
                "Doblemente empotrada"], 
        state="readonly"
        )
    
    entry_tipo_viga.grid(row=0, column=1, padx=5, pady=5)
   
    tipo_viga_var.trace("w", mostrar_campos_apoyos)

    label_apoyo_pat = ttk.Label(viga_frame, text="Coordenada del apoyo móvil [m]:", anchor="w")
    entry_apoyo_pat = ttk.Entry(viga_frame)

    label_apoyo_fijo = ttk.Label(viga_frame, text="Coordenada del apoyo fijo [m]:", anchor="w")
    entry_apoyo_fijo = ttk.Entry(viga_frame)


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

    fuerzas_frame = ttk.Frame(datos_frame, padding=10)
    fuerzas_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    label_carga = ttk.Label(fuerzas_frame, text="Magnitud de la carga [N]:", anchor="w")
    label_carga.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_carga = ttk.Entry(fuerzas_frame)
    entry_carga.grid(row=0, column=1, padx=5, pady=5)

    label_x = ttk.Label(fuerzas_frame, text="Coordenada de la carga [m]:", anchor="w")
    label_x.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_x = ttk.Entry(fuerzas_frame)
    entry_x.grid(row=1, column=1, padx=5, pady=5)

    boton_agregar = ttk.Button(
        fuerzas_frame, 
        text="Agregar Fuerza", 
        style="success.TButton", 
        command=agregar_fuerza
        )
    boton_agregar.grid(row=0, column=3, columnspan=2, padx=10, pady=10)

    boton_borrar = ttk.Button(
        fuerzas_frame, 
        text="Borrar Fuerzas", 
        style="danger.TButton", 
        command=borrar_fuerzas
        )
    boton_borrar.grid(row=1, column=3, columnspan=2, padx=10, pady=10)

    boton_graficar = ttk.Button(
        fuerzas_frame, 
        text="Mostrar gráfico", 
        style="info.TButton", 
        command=obtener_datos
        )
    boton_graficar.grid(row=2, column=3, columnspan=2, padx=5, pady=5)

    boton_carga_distribuida = ttk.Button(
        fuerzas_frame, 
        text="Agregar Carga Distribuida", 
        style="success.TButton", 
        command=abrir_ventana_carga_distribuida
        )
    boton_carga_distribuida.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    resultados_frame = ttk.Frame(frame_barra, padding=2, width=860, height=350)
    #!---------------vvvvvvvvvvvvv----restringe al framr para que no se espanda segun el tamaño de su contenido
    resultados_frame.pack_propagate(False)  
    resultados_frame.pack(padx=5, pady=10)
    text_output = ScrolledText(
        resultados_frame,
        wrap="word", 
        height=10, 
        width=100,
        bg="#f8f9fa", 
        fg="#212529", 
        selectbackground="#d0e7ff",  
        selectforeground="black",  
        relief="ridge", 
        borderwidth=2, 
        font=("Helvetica", 12),  
        padx=10, 
        pady=10   
    )
    text_output.pack(fill="x", pady=5)
    Frame_momento = ttk.Frame(frame_barra, padding=2,width=860, height=350)
    Frame_momento.pack_propagate(False) 
    Frame_momento.pack(padx=5, pady=10)
    root.mainloop()