#!/usr/bin/env python3
"""
Program: wordCount.py
Description:
    Reads a file containing words (presumably separated by spaces) and identifies all
    distinct words along with their frequency (i.e., how many times each word appears).
    The results are printed to the screen and saved to a file named
    "WordCountResults.txt". All computations are performed using basic algorithms,
    not relying on advanced functions or libraries.
    The program handles invalid data in the file by printing errors to the console and
    continuing the execution.
    At the end, the elapsed time for execution and data processing is displayed.
Usage:
    python wordCount.py fileWithData.txt
"""

import sys
import time


def read_words(file_name):
    """
    Reads a file and extracts words separated by whitespace using a basic algorithm.
    If a line is empty or if any error occurs during reading, an error message is printed,
    and the process continues.
    
    Parameters:
        file_name (str): The name of the file to read.
    
    Returns:
        list: A list of words extracted from the file.
    """
    words = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                # Remove leading/trailing whitespace.
                line = line.strip()
                if not line:
                    continue
                # Split the line into words using a basic algorithm.
                current_word = ""
                for char in line:
                    if char.isspace():
                        if current_word != "":
                            words.append(current_word)
                            current_word = ""
                    else:
                        current_word += char
                if current_word != "":
                    words.append(current_word)
    except OSError as e:
        print(f"Error reading file '{file_name}': {e}")
        sys.exit(1)
    return words


def count_words(words):
    """
    Counts the frequency of each distinct word in the list using a basic algorithm.
    The counting is done case-insensitively.
    
    Parameters:
        words (list): List of words.
    
    Returns:
        dict: A dictionary with words as keys and their frequency as values.
    """
    freq = {}
    for word in words:
        # Convert to lower case for case-insensitive counting.
        w = ""
        for char in word:
            # Simple lower-case conversion for ASCII letters.
            if 'A' <= char <= 'Z':
                w += chr(ord(char) + 32)
            else:
                w += char
        # Basic algorithm for counting frequency.
        if w in freq:
            freq[w] = freq[w] + 1
        else:
            freq[w] = 1
    return freq


def format_results(freq, elapsed_time):
    """
    Formats the word frequency dictionary and elapsed time into a result string.
    
    Parameters:
        freq (dict): Dictionary of word frequencies.
        elapsed_time (float): Elapsed time in seconds.
    
    Returns:
        str: Formatted result string.
    """
    results = []
    results.append("Word Count Results:")
    # Ordenamos las palabras alfabéticamente
    keys = list(freq.keys())
    # Algoritmo de ordenamiento simple (bubble sort) para cumplir con "básico"
    n = len(keys)
    for i in range(n):
        for j in range(0, n - i - 1):
            if keys[j] > keys[j + 1]:
                keys[j], keys[j + 1] = keys[j + 1], keys[j]
    for word in keys:
        results.append(f"Word: '{word}' -> Frequency: {freq[word]}")
    results.append(f"Time Elapsed: {elapsed_time:.6f} seconds")
    return "\n".join(results)


def save_results(results_text, output_file):
    """
    Saves the results text to the specified output file.
    
    Parameters:
        results_text (str): The results as a text string.
        output_file (str): The file where the results will be saved.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(results_text)
    except OSError as e:
        print(f"Error writing to file '{output_file}': {e}")


def main():
    """
    Main function of the program.
    Reads the input file provided as a command line parameter, counts the distinct words,
    prints the results to the screen, saves them to 'WordCountResults.txt', and displays the
    elapsed time for execution.
    """
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    words = read_words(input_file)
    freq = count_words(words)
    end_time = time.time()
    elapsed_time = end_time - start_time

    results_text = format_results(freq, elapsed_time)
    print(results_text)
    save_results(results_text, "WordCountResults.txt")


if __name__ == "__main__":
    main()
