#!/usr/bin/env python3
"""
Programa: computeStatistics.py
Descripción:
    Lee un archivo que contiene números (uno por línea), calcula estadísticas descriptivas:
    media, mediana, moda, varianza muestral y desviación estándar usando algoritmos básicos.
    Los resultados se imprimen en pantalla y se guardan en 'StatisticsResults.txt'.
    Las líneas con datos inválidos se reportan en la consola y la ejecución continúa.
    Se muestra el tiempo de ejecución al final.
Uso:
    python computeStatistics.py archivoConDatos.txt
"""

import sys
import time


def quicksort(arr):
    """
    Ordena una lista utilizando el algoritmo de quicksort.
    
    Parámetros:
        arr (list): Lista de números a ordenar.
    
    Retorna:
        list: Lista ordenada.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = []
    middle = []
    right = []
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)
    return quicksort(left) + middle + quicksort(right)


def sqrt_newton(x):
    """
    Calcula la raíz cuadrada de x usando el método de Newton.
    
    Parámetros:
        x (float): Número del que se desea calcular la raíz cuadrada.
    
    Retorna:
        float: Raíz cuadrada de x.
    
    Lanza:
        ValueError: Si x es negativo.
    """
    if x < 0:
        raise ValueError("No se puede calcular la raíz cuadrada de un número negativo.")
    if x == 0:
        return 0
    guess = x
    # Se realizan 20 iteraciones para lograr la convergencia.
    for _ in range(20):
        guess = (guess + x / guess) / 2
    return guess


def main():
    # Se inicia la medición del tiempo de ejecución.
    start_time = time.time()

    # Verifica que se haya pasado exactamente un parámetro (el nombre del archivo).
    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    file_name = sys.argv[1]
    data = []

    # Se abre el archivo de entrada.
    try:
        with open(file_name, "r") as file_handle:
            line_number = 0
            for line in file_handle:
                line_number += 1
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Se omiten las líneas vacías.
                try:
                    # Se intenta convertir la línea a número flotante.
                    number = float(stripped_line)
                    data.append(number)
                except ValueError:
                    # Se reporta en la consola si la línea contiene datos inválidos.
                    print(
                        f"Datos inválidos en la línea {line_number}: "
                        f"'{stripped_line}' no es un número válido."
                    )
                    continue
    except Exception as e:
        print(f"Error al abrir el archivo {file_name}: {e}")
        sys.exit(1)

    # Verifica que se hayan leído números válidos.
    if len(data) == 0:
        print("No se encontraron números válidos en el archivo.")
        sys.exit(1)

    # Calcula la media: suma de todos los números dividida entre la cantidad.
    total = 0
    count = 0
    for num in data:
        total += num
        count += 1
    mean_value = total / count

    # Calcula la mediana.
    sorted_data = quicksort(data)
    if count % 2 == 1:
        median_value = sorted_data[count // 2]
    else:
        median_value = (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2

    # Calcula la moda contando la frecuencia de cada número.
    frequency = {}
    for num in data:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    max_freq = 0
    for key in frequency:
        if frequency[key] > max_freq:
            max_freq = frequency[key]

    modes = []
    for key in frequency:
        if frequency[key] == max_freq:
            modes.append(key)

    # Si todos los números aparecen la misma cantidad de veces, no hay una moda única.
    if len(modes) == len(frequency):
        mode_result = "No hay moda única"
    elif len(modes) == 1:
        mode_result = modes[0]
    else:
        mode_result = modes  # Se muestra una lista de modas si hay más de una.

    # Calcula la varianza muestral:
    # Se utiliza (n - 1) en lugar de n para el cálculo.
    sum_squared_diff = 0
    for num in data:
        diff = num - mean_value
        sum_squared_diff += diff * diff

    if count > 1:
        variance_value = sum_squared_diff / (count - 1)
    else:
        variance_value = 0

    # Calcula la desviación estándar usando el método de Newton para obtener la raíz cuadrada.
    std_deviation = sqrt_newton(variance_value)

    # Calcula el tiempo transcurrido de la ejecución.
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Prepara los resultados para mostrar y guardar.
    results = []
    results.append("Estadísticas Descriptivas:")
    results.append(f"Cantidad: {count}")
    results.append(f"Media: {mean_value}")
    results.append(f"Mediana: {median_value}")
    results.append(f"Moda: {mode_result}")
    results.append(f"Varianza Muestral: {variance_value}")
    results.append(f"Desviación Estándar: {std_deviation}")
    results.append(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")

    results_text = "\n".join(str(item) for item in results)

    # Imprime los resultados en la consola.
    print(results_text)

    # Escribe los resultados en el archivo StatisticsResults.txt.
    try:
        with open("StatisticsResults.txt", "w") as out_file:
            out_file.write(results_text)
    except Exception as e:
        print(f"Error al escribir el archivo de resultados: {e}")


if __name__ == "__main__":
    main()
