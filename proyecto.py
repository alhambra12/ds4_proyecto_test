import os
import sys
import subprocess

ruta_base = os.path.dirname(os.path.abspath(__file__))

def start_json_gen():
    ''' Función para ejecutar el generador de json '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'json_gen', 'app.py'),
        '--dir_datos', os.path.join(ruta_base, 'datos'),
        '--json_file', 'revistas.json'
    ])

def start_scrapper():
    ''' Función para ejecutar el scrapper de scimagojr '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'scrapper', 'app.py'),
        '--dir_json', os.path.join(ruta_base, 'datos', 'json'),
        '--input', 'revistas.json',
        '--output', 'salida.json'
    ])

def start_webapp():
    ''' Función para ejecutar la aplicación web '''

def main():
    ''' Función principal '''
    print("\n¿Qué programa deseas ejecutar?")
    print("1. Ejecutar JSON Generator")
    print("2. Ejecutar Scrapper")
    print("3. Ejecutar WebApp")
    print("4. Salir")

    opcion = input("Selecciona una opción: ").strip()

    match opcion:
        case '1':
            start_json_gen()
        case '2':
            start_scrapper()
        case '3':
            start_webapp()
        case '4':
            print("\nSaliendo del programa.\n")
        case _:
            print("\nOpción no válida.\n")

if __name__ == '__main__':
    main()
