from funct import realizar_calculos, graficar_curvas

opcion=input(f"Ingresar curvas:\n 1. Ingresar curvas \n 2. Calcular regresión: \n Otro: salir\n")

match opcion:
    case "1":
        #valores de la demanda
        valores_P=[4,5,6,7,8,9]
        valores_Q=[135,104,81,68,53,39]
        b0d, b1d= realizar_calculos(valores_P, valores_Q, len(valores_P))
        #valores de la oferta
        valores_P=[4,5,6,7,8,9]
        valores_Q=[26,53,81,98,110,121]
        b0s, b1s=realizar_calculos(valores_P, valores_Q, len(valores_P))
        print(f'valores demanda: {b0d,b1d}')
        print(f'valores oferta: {b0s,b1s}')
        graficar_curvas(b0d, b1d, b0s, b1s)  


    case "2":
        b0d=15000
        b1d=-2500
        b0s=2000
        b1s=7500
        graficar_curvas(b0d, b1d, b0s, b1s)
    case _:
        exit()



