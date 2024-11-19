import matplotlib.pyplot as plt

def graficar_viga(datos, long):
    altura_viga = 0.02 * long  # Ajuste en la altura para una mejor visualización

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(-0.1 * long, 1.1 * long)
    ax.set_ylim(-3 * altura_viga, 4 * altura_viga)

    # Dibujar la viga
    rect = plt.Rectangle((0, 0), long, altura_viga, color='#8A4C29')
    ax.add_patch(rect)

    # Etiquetas de los extremos de la viga
    ax.text(0, -altura_viga * 1.5, 'Inicio de la Viga', ha='center', color='gray')
    ax.text(long, -altura_viga * 1.5, 'Final de la Viga', ha='center', color='gray')

    # Graficar cada fuerza con flechas de tamaño constante
    for carga, x in datos:
        if carga > 0:
            y_inicial = altura_viga
            dy = 1
            color = 'blue'
        else:
            y_inicial = 0
            dy = -1
            color = 'red'

        # Dibujar la flecha con tamaño constante
        ax.arrow(
            x, y_inicial, 0, dy * 0.2,  # Longitud constante para la flecha
            width=0.05, head_width=0.15, head_length=0.1,
            fc=color, ec=color
        )

        # Línea punteada para la posición de la fuerza
        ax.plot([x, x], [0, y_inicial + dy * 0.2], 'k--', linewidth=0.5)

        # Texto con el valor de la carga
        ax.text(
            x, y_inicial + dy * (0.25),  # Ajuste de posición para el texto
            f'{carga} N', ha='center', va='bottom' if dy > 0 else 'top',
            color=color
        )

    # Título y etiquetas
    ax.set_title('Gráfico de la Viga con Cargas Aplicadas')
    ax.set_xlabel('Longitud de la viga (m)')
    ax.axis('off')  # Oculta los ejes para un diseño más limpio

    plt.show()


datos = [
    [100, 2],
    [-50, 5],
    [30, 1],
    [8000,3],
    [2500,4],
    [-45,1.5]
]

graficar_viga(datos, 10)