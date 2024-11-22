def reacciones_simlemente_apoyada(fuerzas, longitud, x_apoyo_movil, x_apoyo_fijo):
    R_A = 0.0
    R_B = 0.0
    
    suma_fuerzas = sum([fuerza[0] for fuerza in fuerzas])
    
    suma_momentos = 0.0
    for fuerza in fuerzas:
        F = fuerza[0]
        x = fuerza[1]
        suma_momentos += F * x
    
    R_B = suma_momentos / longitud
    
    R_A = suma_fuerzas - R_B
    
    return [R_A, R_B]

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


def calcular_reacciones(tipo_viga, fuerzas, longitud, x_apoyo_movil=None, x_apoyo_fijo=None):
    if tipo_viga == "Simplemente apoyada":
        R_A, R_B = reacciones_simlemente_apoyada(fuerzas, longitud, x_apoyo_movil, x_apoyo_fijo)

    elif tipo_viga == "Viga en voladizo":
        R_A, M_A = reacciones_voladizo(fuerzas, longitud)
        print(R_A)

    elif tipo_viga == "Doblemente empotrada":
        R_A, R_B, M_A, M_B = reacciones_empotrada(fuerzas, longitud)

    else:
        raise ValueError("Tipo de viga no reconocido. Los valores válidos son: 'Simplemente apoyada', 'Viga en voladizo', 'Doblemente empotrada'.")



tipo = "Viga en voladizo"
fuerzas = [[100, 5]] 
longitud = 10  
x_apoyo_movil = 0
x_apoyo_fijo = 10

reacciones = calcular_reacciones(tipo, fuerzas, longitud, x_apoyo_movil, x_apoyo_fijo)
print(reacciones)

