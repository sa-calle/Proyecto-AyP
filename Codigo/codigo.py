def ingreso_fuerza():
    n = 1 # nuemero de fuerzas
    datos = [] 
    fuerza = [0.0,0.0,0.0]
    for i in range(1,n+1,1):
        while ValueError != None:
            try:
                fuerza[0] = float(input('ingrese la carga de la viga: '))
                fuerza[1] = float(input('ingrese la cordenada en x de la fuerza: '))
                while fuerza[1] < 0:
                    fuerza[1] = float(input('ingrese una curdenada positiva: '))
                fuerza[2] = float(input('ingrese el tipo de viga, 0 para carga puntual, 1 pra carga distribuida: '))
                datos.append(fuerza)
            except ValueError:
                print('Error se ingreso un valor que no es valido')

    return(datos)       
            
datos = ingreso_fuerza()
print(datos)