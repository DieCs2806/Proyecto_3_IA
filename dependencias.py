class Nodo:
    def __init__(self, nombre, dependencias, probabilidades, opciones):
        self.nombre = nombre
        self.dependencias = dependencias
        self.probabilidades = probabilidades
        self.opciones = opciones
    

class Grafo:
    def __init__(self):
        self.nodos = {} 

    def añadirNodo(self, nodo):
        if not isinstance(nodo, Nodo):
            raise TypeError("El objeto debe ser de tipo Nodo")
        
        if nodo.nombre in self.nodos:
            raise ValueError("El nodo ya existe")
            
        self.nodos[nodo.nombre] = nodo
    def obtener_padres(self, nombre_nodo):
        """Devuelve la lista de nombres de los nodos padres."""
        if nombre_nodo not in self.nodos:
            raise ValueError("El nodo no está en el grafo")
            
        return self.nodos[nombre_nodo].dependencias

    def obtener_hijos(self, nombre_nodo):
        """Devuelve una lista de los nodos hijos."""
        hijos = []
        for nombre, nodo in self.nodos.items():
            if nombre_nodo in nodo.dependencias:
                hijos.append(nombre)
        return hijos