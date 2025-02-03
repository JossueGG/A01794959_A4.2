#!/usr/bin/env python3
# pylint: disable=invalid-name
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


def read_data(file_name):
    """
    Lee un archivo y retorna una lista de números (float). Se ignoran las líneas vacías y 
    se reportan datos inválidos.

    Parámetros:
        file_name (str): Nombre del archivo a leer.

    Retorna:
        list: Lista de números leídos.
    """
    data = []
    try:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            for i, line in enumerate(file_handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    number = float(line)
                    data.append(number)
                except ValueError:
                    print(
                        f"Datos inválidos en la línea {i}: '{line}' no es un número válido."
                    )
    except OSError as e:
        print(f"Error al abrir el archivo {file_name}: {e}")
        sys.exit(1)
    return data


def calculate_mean(data):
    """
    Calcula la media de una lista de números.

    Parámetros:
        data (list): Lista de números.

    Retorna:
        float: La media.
    """
    total = 0
    count = 0
    for num in data:
        total += num
        count += 1
    return total / count if count > 0 else 0


def calculate_median(data):
    """
    Calcula la mediana de una lista de números.

    Parámetros:
        data (list): Lista de números.

    Retorna:
        float: La mediana.
    """
    sorted_data = quicksort(data)
    n = len(sorted_data)
    if n % 2 == 1:
        return sorted_data[n // 2]
    return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


def calculate_mode(data):
    """
    Calcula la moda de una lista de números.

    Parámetros:
        data (list): Lista de números.

    Retorna:
        La moda, ya sea un valor único, una lista de valores o una cadena indicando que 
        no hay moda única.
    """
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1

    max_freq = max(frequency.values(), default=0)
    modes = [num for num, freq in frequency.items() if freq == max_freq]

    if len(modes) == len(frequency):
        return "No hay moda única"
    if len(modes) == 1:
        return modes[0]
    return modes


def calculate_variance(data, mean_value):
    """
    Calcula la varianza muestral de una lista de números.

    Parámetros:
        data (list): Lista de números.
        mean_value (float): La media de los números.

    Retorna:
        float: La varianza muestral.
    """
    n = len(data)
    if n <= 1:
        return 0
    sum_squared_diff = 0
    for num in data:
        diff = num - mean_value
        sum_squared_diff += diff * diff
    return sum_squared_diff / (n - 1)


def compute_statistics(data):
    """
    Calcula las estadísticas descriptivas de una lista de números.

    Parámetros:
        data (list): Lista de números.

    Retorna:
        dict: Diccionario con las estadísticas: cantidad, media, mediana, moda, varianza 
        muestral y desviación estándar.
    """
    stats = {}
    stats["count"] = len(data)
    stats["mean"] = calculate_mean(data)
    stats["median"] = calculate_median(data)
    stats["mode"] = calculate_mode(data)
    stats["variance"] = calculate_variance(data, stats["mean"])
    stats["std_deviation"] = sqrt_newton(stats["variance"])
    return stats


def save_results(results_text, file_name):
    """
    Guarda los resultados en un archivo.

    Parámetros:
        results_text (str): Texto de los resultados.
        file_name (str): Nombre del archivo donde se guardarán los resultados.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as out_file:
            out_file.write(results_text)
    except OSError as e:
        print(f"Error al escribir el archivo de resultados: {e}")


def main():
    """
    Función principal del programa.
    Se encarga de leer los datos, calcular las estadísticas, imprimir y guardar los
    resultados.
    """
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    data = read_data(input_file)

    if not data:
        print("No se encontraron números válidos en el archivo.")
        sys.exit(1)

    stats = compute_statistics(data)
    end_time = time.time()
    elapsed_time = end_time - start_time

    results_lines = [
        "Estadísticas Descriptivas:",
        f"Cantidad: {stats['count']}",
        f"Media: {stats['mean']}",
        f"Mediana: {stats['median']}",
        f"Moda: {stats['mode']}",
        f"Varianza Muestral: {stats['variance']}",
        f"Desviación Estándar: {stats['std_deviation']}",
        f"Tiempo de Ejecución: {elapsed_time:.6f} segundos",
    ]
    results_text = "\n".join(results_lines)

    print(results_text)
    save_results(results_text, "StatisticsResults.txt")


if __name__ == "__main__":
    main()
