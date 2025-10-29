import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dependencias import Nodo,Grafo
import csv
from typing import List, Dict, Any

def numDep(lector):
      contador = 0
      n = Nodo()
      linea = next(lector)
      linea2 = next(lector)
      for palabra in linea2:
            if not isinstance(palabra, float):
                    contador = contador+1
            return contador

def leerArchivo(nomArch):
        with open(nomArch, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            n = Nodo(lector)
            linea1 = next(lector)
            nDep = numDep()
            dependencias = [h.strip() for h in linea1[:nDep]]
            opciones = [h.strip() for h in linea1[nDep:]]


