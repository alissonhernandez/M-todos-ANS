import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas con el hilo principal

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import sympy as sp
import pandas as pd

def diferencias_divididas(x, fx, fdx):
    n = len(x)  # Cantidad de puntos
    z = np.empty(shape=2 * n, dtype=float) # Vector de puntos z (repetidos, columna vertical de X)
    fz = np.zeros(shape=(2 * n, 2 *  n), dtype=float) # Matriz de diferencias divididas (cada columna es una diferencia dividida), se inicializa con ceros
    df_text = pd.DataFrame(np.full((2 * n, 2 * n), '0', dtype=object)) # DataFrame para mostrar los cálculos realizados
    # Crear el vector z y la matriz de diferencias divididas
    for i in np.arange(n):
        z[2 * i] = x[i] # Puntos x repetidos
        z[2 * i + 1] = x[i] # Puntos x repetidos
        fz[2 * i][0] = fx[i] # Puntos f(x)
        fz[2 * i + 1][0] = fx[i] # Puntos f(x)
        fz[2 * i + 1][1] = fdx[i] # Puntos f'(x)
        #df_text.at[2 * i, 0] = f"fx[{i}] = {fx[i]}"
        #df_text.at[2 * i + 1, 0] = f"fx[{i}] = {fx[i]}"
        #df_text.at[2 * i + 1, 1] = f"fdx[{i}] = {fdx[i]}"
        df_text.at[2 * i, 0] = f"{fx[i]}" # Puntos f(x) en el DataFrame
        df_text.at[2 * i + 1, 0] = f"{fx[i]}" # Puntos f(x) en el DataFrame
        df_text.at[2 * i + 1, 1] = f"{fdx[i]}" # Puntos f'(x) en el DataFrame
        if i != 0: # Calcular las diferencias divididas
            operation = f"({fz[2 * i][0]} - {fz[2 * i - 1][0]}) / ({z[2 * i]} - {z[2 * i - 1]})" # Operación a realizar para obtener la diferencia dividida
            result = (fz[2 * i][0] - fz[2 * i - 1][0]) / (z[2 * i] - z[2 * i - 1]) # Resultado de la diferencia dividida (f[x0, x1])
            fz[2 * i][1] = result # Asignar el resultado a la matriz de diferencias divididas
            df_text.at[2 * i, 1] = f"{operation} = {result}" # Asignar la operación y el resultado al DataFrame
    # Calcular las diferencias divididas
    for i in np.arange(2, 2 * (n - 1) + 2): # Recorrer las columnas de la matriz de diferencias divididas (empezando desde la tercera columna)
        for j in np.arange(2, i + 1): # Recorrer las filas de la matriz de diferencias divididas (empezando desde la tercera fila)
            f = fz[i][j - 1] - fz[i - 1][j - 1] # Calcular la diferencia dividida (f[x0, x1, ..., xj])
            g = z[i] - z[i - j] # Calcular el denominador de la diferencia dividida
            result = f / g # Calcular la diferencia dividida
            fz[i][j] = result # Asignar el resultado a la matriz de diferencias divididas
            operation = f"({fz[i][j - 1]} - {fz[i - 1][j - 1]}) / ({z[i]} - {z[i - j]})" # Operación a realizar para obtener la diferencia dividida
            df_text.at[i, j] = f"{operation} = {result}" # Asignar la operación y el resultado al DataFrame

    d = fz.diagonal() # Obtener la diagonal de la matriz de diferencias divididas (diferencias divididas de orden 0)

    # Crear DataFrame de las diferencias divididas
    fz_df = pd.DataFrame(fz)

    # Asignar nombres de columnas al DataFrame
    fz_df.columns = [f"f{'\''*i}(X{i})" for i in range(2 * n)]
    df_text.columns = [f"f{'\''*i}(X{i})" for i in range(2 * n)]

    return z, d, fz_df, df_text # Retornar los puntos z, las diferencias divididas de orden 0, la matriz de diferencias divididas y el DataFrame de los cálculos realizados


def polinomio_hermite(diff, z):
    x = sp.symbols('x')  # Variable simbólica
    n = len(z) # Cantidad de puntos
    pol = diff[0] # Polinomio de Hermite
    terminos_subs = [f"{diff[0]}"] # Términos del polinomio
    # Crear los pasos para encontrar el polinomio de Hermite
    pasos = ['Para encontrar el polinomio haremos uso de la siguiente ecuación: P(x) = f[X0] + f[X1](X-X0) + f[X2](X-X0)(X-X1) + f[X3](X-X0)(X-X1)(X-X2)...', 
             f"Paso 1: P(x0) = {diff[0]}"]
    terminos = [diff[0]] # Términos del polinomio
    # Calcular los términos del polinomio de Hermite
    for k in range(1, n):
        term = diff[k] # Término actual del polinomio
        term_details = f"{diff[k]}" # Detalles del término actual
        for j in range(k): # Recorrer los puntos anteriores al punto actual
            term *= (x - z[j]) # Multiplicar el término actual por (x - Xj)
            term_details += f" * (x - ({z[j]}))" # Añadir el término actual a los detalles
        terminos.append(term) # Añadir el término actual a la lista de términos
        terminos_subs.append(f"{diff[k]}{'*'.join([f'(x - ({z[j]}))' for j in range(k)])}") # Añadir el término actual a la lista de términos sustituidos
        pol = sp.Add(*terminos) # Polinomio actual de Hermite
        paso_detallado = f"Paso {k + 1}: Añadiendo término {k}: {term_details} realizando las operaciones obtenemos: {sp.expand(term)}" # Paso detallado
        pol_actual = f"P(x{k}) = {' + '.join([str(t) for t in terminos])}" # Polinomio actual de Hermite en formato de cadena
        pasos.append(f"{paso_detallado}") # Añadir el paso detallado a la lista de pasos
        pasos.append(f"Polinomio actual: {pol_actual}") # Añadir el polinomio actual a la lista de pasos
    
    pol_expandido = sp.expand(pol) # Polinomio de Hermite expandido
    pasos.insert(1, f"Sustituyendo: P(x) = {' + '.join(terminos_subs)}") # Añadir el paso de sustitución a la lista de pasos
    pasos.append(f"Realizando correspondientes, obtenemos que: P(x) = {pol_expandido}") # Añadir el paso final a la lista de pasos
    return pol_expandido, pasos # Retornar el polinomio de Hermite y los pasos para encontrarlo

def graficar_hermite(x, fx, pol):
    # Crear los valores de x para evaluar el polinomio los cuales van desde el mínimo valor de x hasta el máximo valor de x
    x_vals = np.linspace(min(x) - 2, max(x) + 2, 100)
    y_vals = [pol.subs('x', val) for val in x_vals] # Evaluar el polinomio en los valores de x

    # Dibujar la gráfica
    plt.plot(x, fx, 'o', label='Puntos') # Dibujar los puntos dados
    plt.plot(x_vals, y_vals, label='Polinomio') # Dibujar el polinomio de Hermite
    plt.axhline(0, color='black')  # Agrega una línea horizontal en y=0 
    plt.axvline(0, color='black')  # Agrega una línea vertical en x=0
    # Etiquetas de los puntos
    for i in range(len(x)):
        plt.text(x[i], fx[i], f'({x[i]}, {fx[i]})') # Etiquetas de los puntos (x, f(x))

    plt.legend() # Agregar la leyenda
    plt.title('Interpolación de Hermite') # Título de la gráfica
    plt.xlabel('x') # Etiqueta del eje x
    plt.ylabel('f(x)') # Etiqueta del eje y

    # Crea la imagen de la gráfica
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) # Mover el cursor al inicio del archivo
    # Codifica la imagen en base64
    img_str = base64.b64encode(buffer.read())
    plt.close()

    return img_str.decode() # Retornar la imagen en base64