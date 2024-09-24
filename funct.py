import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

def calcular_sumatorias(variable_independiente, variable_dependiente, registros):
    suma_x = sum(variable_independiente)
    suma_y = sum(variable_dependiente)
    suma_x2 = sum([x**2 for x in variable_independiente])
    suma_y2 = sum([y**2 for y in variable_dependiente])
    suma_xy = sum([variable_independiente[i] * variable_dependiente[i] for i in range(registros)])
    return suma_x, suma_y, suma_x2, suma_xy, suma_y2

# Función para calcular b1 (pendiente)
def calcular_b1(suma_x, suma_y, suma_x2, suma_xy, registros):
    b1 = (suma_xy - ((suma_x * suma_y) / registros)) / (suma_x2 - (suma_x**2) / registros)
    return b1

# Función para calcular b0 (intercepto)
def calcular_b0(suma_x, suma_y, b1, registros):
    b0 = (1/registros) * (suma_y - (b1 * suma_x))
    return b0

def realizar_calculos(valores_q, valores_p, n):
    suma_x, suma_y, suma_x2, suma_xy, suma_y2=calcular_sumatorias(valores_q, valores_p, n)
    b1=calcular_b1(suma_x, suma_y, suma_x2, suma_xy, n)
    b0=calcular_b0(suma_x, suma_y, b1, n)
    return b0, b1



def graficar_curvas(b0d, b1d, b0s, b1s):
    P_equilibrio, Q_equilibrio = calcular_equilibrio(b0d, b1d, b0s, b1s)
    print(f"Precio de equilibrio:{P_equilibrio}, Cantidad de equilibrio:{Q_equilibrio}")
    # Calcular interceptos para la curva de demanda
    P_d_intercepto = -b0d / b1d  # Intercepto con el eje de precios para demanda
    Q_d_intercepto = b0d  # Intercepto con el eje de cantidad para demanda

    # Calcular interceptos para la curva de oferta
    P_s_intercepto = -b0s / b1s  # Intercepto con el eje de precios para oferta
    Q_s_intercepto = b0s  # Intercepto con el eje de cantidad para oferta

    ec,ep=Calcular_excedentes(Q_equilibrio, P_equilibrio, P_d_intercepto, Q_s_intercepto, P_s_intercepto )
    print(f"Excedente del consumidor: {ec}, Excedente del productor: {ep}")
    # Crear un rango de precios basado en los interceptos
    P = np.linspace(0, max(P_d_intercepto, P_s_intercepto), 100)

    # Calcular las cantidades usando las ecuaciones de las rectas
    Q_d = b0d + b1d * P  # Ecuación de la demanda
    Q_s = b0s + b1s * P  # Ecuación de la oferta

    # Crear la gráfica
    plt.figure(figsize=(10, 10))
    plt.plot(Q_d, P, label='Curva de Demanda', color='blue')
    plt.plot(Q_s, P, label='Curva de Oferta', color='red')


    # Añadir los puntos de los interceptos
    plt.scatter([Q_d_intercepto], [0], color='blue', marker='o', label=f'Intercepto Demanda (0, {Q_d_intercepto:.2f})')
    plt.scatter([0], [P_d_intercepto], color='blue', marker='x', label=f'Intercepto Precio Demanda ({P_d_intercepto:.2f}, 0)')
    
    plt.scatter([Q_s_intercepto], [0], color='red', marker='o', label=f'Intercepto Oferta (0, {Q_s_intercepto:.2f})')
    plt.scatter([0], [P_s_intercepto], color='red', marker='x', label=f'Intercepto Precio Oferta ({P_s_intercepto:.2f}, 0)')

    # Si se ha calculado el punto de equilibrio, añadirlo a la gráfica
    if P_equilibrio is not None and Q_equilibrio is not None:
        # Dibujar las líneas vertical y horizontal en el punto de equilibrio
        plt.axhline(P_equilibrio, color='green', linestyle='--', label=f'Equilibrio Precio (P={P_equilibrio:.2f})')
        plt.axvline(Q_equilibrio, color='green', linestyle='--', label=f'Equilibrio Cantidad (Q={Q_equilibrio:.2f})')

        # Añadir el punto de equilibrio
        plt.scatter([Q_equilibrio], [P_equilibrio], color='green', marker='o', label=f'Punto de Equilibrio ({P_equilibrio:.2f}, {Q_equilibrio:.2f})')

    # Configuración de la gráfica
    plt.title('Curvas de Oferta y Demanda con Interceptos y Punto de Equilibrio')
    plt.xlabel('Precio (P)')
    plt.ylabel('Cantidad (Q)')
    plt.axhline(0, color='red', lw=0.5, ls='--')  # Eje horizontal
    plt.axvline(0, color='red', lw=0.5, ls='--')  # Eje vertical
    plt.legend()
    plt.grid(True)

    # Ajustar los límites de los ejes para que muestren todos los puntos relevantes
    plt.xlim(0, max(Q_d_intercepto, Q_s_intercepto, Q_equilibrio) * 1.1)  # Ajuste del eje de cantidades
    plt.ylim(0, max(P_d_intercepto, P_s_intercepto, P_equilibrio) * 1.1)  # Ajuste del eje de precios

    tick_interval_x = (plt.xlim()[1] - plt.xlim()[0]) / 15  # Establecer un intervalo basado en el rango de Q
    tick_interval_y = (plt.ylim()[1] - plt.ylim()[0]) / 15  # Establecer un intervalo basado en el rango de P

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_interval_x))  # Ajusta el intervalo de los ticks del eje x
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(tick_interval_y))  # Ajusta el intervalo de los ticks del eje y

    
    # Mostrar la gráfica
    plt.show()

def calcular_equilibrio(b0d, b1d, b0s, b1s):
    # Cálculo del precio y cantidad de equilibrio
    P_equilibrio = (b0s - b0d) / (b1d - b1s)
    Q_equilibrio = b0d + b1d * P_equilibrio
    return P_equilibrio, Q_equilibrio

def Calcular_excedentes(Q_eq, P_eq, P_d_int, Q_s_int, P_s_int ):
    ec= (Q_eq*(P_d_int-P_eq))/2
    ep=0
    if Q_s_int>0:
        ep=((Q_eq+Q_s_int)*P_eq)/2
    else:
        ep=(Q_eq(P_eq-P_s_int))/2
    return ec,ep