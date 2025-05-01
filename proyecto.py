import os
import sys
import subprocess

ruta_base = os.path.dirname(os.path.abspath(__file__))

def ejecutar_json_gen():
    ''' Función para ejecutar el generador de json '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'json_gen', 'app.py'),
        '--dir_datos', os.path.join(ruta_base, 'datos'),
        '--archivo_json', 'revistas.json'
    ])

def ejecutar_scrapper():
    ''' Función para ejecutar el scrapper de scimagojr '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'scrapper', 'app.py'),
        '--dir_json', os.path.join(ruta_base, 'datos', 'json'),
        '--json_entrada', 'revistas.json',
        '--json_salida', 'salida.json'
    ])

def ejecutar_webapp():
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
            ejecutar_json_gen()
        case '2':
            ejecutar_scrapper()
        case '3':
            ejecutar_webapp()
        case '4':
            print("\nSaliendo del programa.\n")
        case _:
            print("\nOpción no válida.\n")

if __name__ == '__main__':
    main()
