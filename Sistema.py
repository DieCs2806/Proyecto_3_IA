import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dependencias import Nodo,Grafo
import csv
from typing import List, Dict, Any, Tuple


def numDep(lector: Any) -> int:
    try:
        linea2 = next(lector) #Es la linea 2 porque en la función grande ya leímos la 1 en el lector
        nDep = 0
        for i, valor in enumerate(linea2):
            try:
                float(valor.strip()) #Cada que sea un valor flotante 
                nDep = i
                return nDep
            except ValueError:
                continue
        return len(linea2)
    except StopIteration:
        return 0


def leerArchivo(nomArch: str):
    try:
        with open(nomArch, 'r', encoding='utf-8') as archivo:
            nombre = nomArch[:-4]
            lector = csv.reader(archivo, skipinitialspace=True)
            encabezados = next(lector)
            nDep = numDep(lector)
            dependencias = [h.strip() for h in encabezados[:nDep]]
            opciones = [h.strip() for h in encabezados[nDep:]]
            print(f"nDep inferido: {nDep}")
            print(f"Dependencias: {dependencias}")
            print(f"Opciones: {opciones}")
            archivo.seek(0) #Volver a la primera linea del archivo
            lector = csv.reader(archivo, skipinitialspace=True)
            next(lector) # Saltar el encabezado
            probabilidades: Dict[Tuple[str], Dict[str, float]] = {}
            for lineas in lector:
                if not lineas:
                    continue
                opcionesDep = tuple(v.strip() for v in lineas[:nDep])
                columnasProb = tuple(float(v.strip()) for v in lineas [nDep:])
                asignacionProb = dict(zip(opciones, columnasProb))
                probabilidades[opcionesDep] = asignacionProb
            nodo = Nodo(nombre, dependencias,probabilidades, opciones)
            return nodo

    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo '{nomArch}'.")
        return None, None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None, None
    
def main():
    nodo_cargado = leerArchivo("Train.csv")
    grafo = Grafo({}, {})
    grafo.añadirNodo(nodo_cargado)
    if nodo_cargado:
        print("\n--- ¡Nodo Cargado Exitosamente! ---")
        print(f"Nombre del Nodo: {nodo_cargado.nombre}")
        print(f"Probabilidades (primeras 3 entradas): {dict(list(nodo_cargado.probabilidades.items())[:6])}")
    else:
        print("\n--- Fallo en la carga del nodo. ---")


if __name__ == "__main__":
    main()
