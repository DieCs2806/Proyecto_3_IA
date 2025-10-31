class Nodo:
    def __init__(self, nombre, dependencias, probabilidades, opciones):
        self.nombre = nombre
        self.dependencias = dependencias
        self.probabilidades = probabilidades
        self.opciones = opciones
    

class Grafo:
    def __init__(self, nodo, conexiones):
        self.nodo = {}
        self.conexiones = {}    
    
    def añadirNodo(self, nodo):
        if not isinstance(nodo, Nodo):
            raise TypeError("El objeto debe ser de tipo Nodo")
        
        if nodo.nombre in self.nodo:
            raise ValueError("El nodo ya existe")
        self.nodo[nodo.nombre] = nodo
    
    