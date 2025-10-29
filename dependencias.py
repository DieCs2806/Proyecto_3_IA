class Nodo:
    def __init__(self, nombre, nDeps,nOpciones, dependencias, probabilidades, opciones):
        self.nombre = nombre
        self.nDeps = nDeps
        self.nOpciones = nOpciones
        self.dependencias = dependencias
        self.probabilidades = probabilidades
        self.opciones = opciones
    

class Grafo:
    def __init__(self, nodo, conexiones):
        self.nodo = nodo
        self.conexiones = conexiones
    
    def añadirNodo(self, nodo):
        if not isinstance(nodo, Nodo):
            raise TypeError("El objeto debe ser de tipo Nodo")
        
        if nodo.nombre in self.nodo:
            raise TypeError("El nodo ya existe")
        self.nodo = nodo
    
    