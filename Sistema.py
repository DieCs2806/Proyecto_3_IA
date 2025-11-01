import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dependencias import Nodo,Grafo
import csv
from typing import List, Dict, Any, Tuple
import pyagrum as agr


def numDep(lector: Any):
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
    
def leer_dependencias(path_csv: str):
    df = pd.read_csv(path_csv)
    arcos = list(df[['Padre', 'Hijo']].itertuples(index=False, name=None))
    return arcos
    
def inferenciaEnumeracion(bn: agr.BayesNet, evidencia: Dict[str, str], consulta: str) -> Dict[str, float]:
    ie = agr.LazyPropagation(bn)
    ie.setEvidence(evidencia)
    resultado = ie.posterior(consulta)
    distribucion = {}
    for i in range(resultado.size()):
        etiqueta = bn.variable(consulta).label(i)
        probabilidad = resultado[i]
        distribucion[etiqueta] = probabilidad
    return distribucion

def main():
    grafo = Grafo()
    nodo_train = leerArchivo("Train.csv")
    nodo_rain = leerArchivo("Rain.csv")
    nodo_appt = leerArchivo("Appoinment.csv")
    nodo_maint = leerArchivo("Maintenance.csv")
    
    if not all([nodo_train, nodo_rain, nodo_appt, nodo_maint]):
         print("Error: No se pudieron cargar todos los archivos de nodos. Terminando.")
         return

    grafo.añadirNodo(nodo_train)
    grafo.añadirNodo(nodo_rain)
    grafo.añadirNodo(nodo_appt)
    grafo.añadirNodo(nodo_maint)
    
    print("\n--- ¡Nodos Cargados en tu Grafo Exitosamente! ---")

    print(f"Probabilidades: {dict(list(nodo_train.probabilidades.items())[0:])}")
    
    bn = agr.BayesNet("RedBayesiana")

    for nombre, nodo in grafo.nodos.items():
        # Crear la variable LabelizedVariable de pyAgrum
        variable = agr.LabelizedVariable(nombre, nombre)
        for opcion in nodo.opciones:
            variable.addLabel(opcion)
        try:
             bn.add(variable) 
             print(f"✅ Variable '{nombre}' (pyAgrum) añadida con opciones: {nodo.opciones}")
        except TypeError as e:
             # Esto captura el error y te da más información si persiste
             print(f"🚨 ERROR: Falló al añadir la variable '{nombre}' a pyAgrum. Detalle: {e}")
             return # Detener si hay un error
    arcos = leer_dependencias('Dependencias.csv')
    print(f"\n--- Añadiendo Arcos a pyAgrum ---")    
    for padre, hijo in arcos:
        try:
             bn.addArc(padre, hijo)
             print(f"🔗 Arco añadido: {padre} -> {hijo}")
        except Exception as e:
             print(f"Error al añadir arco {padre} -> {hijo}: {e}")
    evidencia = {"Rain": "Light", "Maintenance": "No"}
    consulta = "Train"
    VA = inferenciaEnumeracion(bn, evidencia, consulta)
    print(f"\n--- Resultados de la Inferencia para '{consulta}' dado {evidencia} ---")
    for valor, prob in VA.items():
        print(f"P({consulta}={valor} | evidencia) = {prob:.4f}")


if __name__ == "__main__":
    main()

