import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dependencias import Nodo,Grafo
import csv
from typing import List, Dict, Any


def leerArchivo(nomArch):
    df = pd.read_csv(nomArch)
    
