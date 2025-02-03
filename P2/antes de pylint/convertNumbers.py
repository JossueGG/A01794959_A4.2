#!/usr/bin/env python3
"""
Programa: convertNumbers.py
Descripción:
    Lee un archivo que contiene números (uno por línea) y convierte cada número a sus
    representaciones en binario y hexadecimal utilizando algoritmos básicos.
    - Para la conversión a binario:
        • Si el número es negativo, se utiliza un sistema de 10 bits en complemento a dos.
        • Si el número es positivo, se realiza la conversión normal.
    - Para la conversión a hexadecimal:
        • Si el número es negativo, se utiliza un sistema de 32 bits (8 dígitos hexadecimales)
          en complemento a dos.
        • Si el número es positivo, se realiza la conversión de forma normal.
    Los resultados se muestran en pantalla y se guardan en el archivo "ConvertionResults.txt".
    Se manejan datos inválidos mostrando un error en consola y continuando la ejecución.
    Además, se mide y muestra el tiempo de ejecución.
Uso:
    python convertNumbers.py archivoConDatos.txt
"""

import sys
import time


def convert_to_binary(num):
    """
    Convierte un número entero a su representación en binario.
    Para números negativos se utiliza un sistema de 10 bits en complemento a dos;
    para números positivos se realiza la conversión normal.

    Parámetros:
        num (int): Número entero a convertir.
    Retorna:
        str: Cadena que representa el número en binario. Para negativos, se muestran 10 dígitos.
    """
    if num < 0:
        bits = 10
        mask = (1 << bits) - 1  # 2^10 - 1 = 1023
        # Se obtiene la representación en complemento a dos en 10 bits
        value = num & mask
        binary_str = ""
        # Se generan exactamente 'bits' dígitos (de más significativo a menos significativo)
        for i in range(bits):
            bit = (value >> (bits - 1 - i)) & 1
            binary_str += str(bit)
        return binary_str
    else:
        # Conversión normal para números positivos
        if num == 0:
            return "0"
        binary_str = ""
        while num > 0:
            binary_str = str(num % 2) + binary_str
            num //= 2
        return binary_str


def convert_to_hexadecimal(num):
    """
    Convierte un número entero a su representación en hexadecimal.
    Para números negativos se utiliza un sistema de 32 bits (8 dígitos hexadecimales)
    en complemento a dos; para números positivos se realiza la conversión normal.

    Parámetros:
        num (int): Número entero a convertir.
    Retorna:
        str: Cadena que representa el número en hexadecimal.
             Para negativos, se muestran 8 dígitos.
    """
    hex_digits = "0123456789ABCDEF"
    if num < 0:
        bits = 32
        mask = (1 << bits) - 1  # 2^32 - 1
        # Se obtiene la representación en complemento a dos en 32 bits
        value = num & mask
        hex_str = ""
        # 32 bits corresponden a 8 dígitos hexadecimales (4 bits por dígito)
        for _ in range(8):
            digit = value & 0xF
            hex_str = hex_digits[digit] + hex_str
            value //= 16
        return hex_str
    else:
        # Conversión normal para números positivos
        if num == 0:
            return "0"
        hex_str = ""
        while num > 0:
            digit = num % 16
            hex_str = hex_digits[digit] + hex_str
            num //= 16
        return hex_str


def read_numbers(file_name):
    """
    Lee un archivo y extrae números enteros de cada línea.
    Se omiten las líneas vacías y se muestran mensajes de error para datos inválidos.

    Parámetros:
        file_name (str): Nombre del archivo a leer.
    Retorna:
        list: Lista de números enteros válidos.
    """
    numeros = []
    try:
        with open(file_name, "r", encoding="utf-8") as file_handle:
            for i, line in enumerate(file_handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    valor = float(line)
                    if not valor.is_integer():
                        print(f"Datos inválidos en la línea {i}: '{line}' no es un entero.")
                        continue
                    numeros.append(int(valor))
                except ValueError:
                    print(f"Datos inválidos en la línea {i}: '{line}' no es un número válido.")
    except OSError as e:
        print(f"Error al abrir el archivo {file_name}: {e}")
        sys.exit(1)
    return numeros


def save_results(results_text, file_name):
    """
    Guarda el texto de resultados en un archivo.

    Parámetros:
        results_text (str): Texto con los resultados.
        file_name (str): Nombre del archivo donde se guardarán los resultados.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as out_file:
            out_file.write(results_text)
    except OSError as e:
        print(f"Error al escribir el archivo {file_name}: {e}")


def main():
    """
    Función principal del programa.
    Se encarga de leer los datos, convertir los números a binario (10 bits en complemento a dos para negativos)
    y a hexadecimal (32 bits en complemento a dos para negativos), y mostrar y guardar los resultados.
    """
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py archivoConDatos.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    numeros = read_numbers(input_file)

    resultados = []
    resultados.append("Conversiones de Números:")
    for idx, num in enumerate(numeros, start=1):
        binario = convert_to_binary(num)
        hexadecimal = convert_to_hexadecimal(num)
        resultados.append(
            f"Número {idx}: {num} | Binario: {binario} | Hexadecimal: {hexadecimal}"
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    resultados.append(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")

    resultados_texto = "\n".join(resultados)
    print(resultados_texto)
    save_results(resultados_texto, "ConvertionResults.txt")


if __name__ == "__main__":
    main()
