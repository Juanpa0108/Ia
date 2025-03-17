posicion_paquetes = []

class Nodo:
    def __init__(self, estado, padre=None, operador=None, profundidad=0):
        self.estado = estado  
        self.padre = padre  
        self.operador = operador  
        self.profundidad = profundidad 

    def __str__(self):
        return f"Nodo(estado={self.estado}, operador={self.operador}, profundidad={self.profundidad})"


def leer_mapa(archivo_txt):
    with open("archivo.txt", "r") as archivo:
        matriz = [list(map(int, linea.split())) for linea in archivo]
    return matriz

mapa = leer_mapa("archivo.txt")

def encontrar_paquetes(mapa):
    paquetes = []  
    for i, fila in enumerate(mapa):
        for j, valor in enumerate(fila):
            if valor == 4:  
                paquetes.append((i, j))  
    return paquetes

posicion_paquetes = encontrar_paquetes(mapa)

def encontrar_posicion_inicial(mapa):
    for i, fila in enumerate(mapa):  
        for j, valor in enumerate(fila):  
            if valor == 2:  
                return (i, j)  
    return None 

posicion_inicial = encontrar_posicion_inicial(mapa)
nodo_inicial = Nodo(posicion_inicial, None, None, 0)

def mover_derecha(pos, mapa):
    fila, columna = pos
    if columna + 1 < len(mapa[0]) and mapa[fila][columna + 1] != 1:
        return (fila, columna + 1)
    return None

def mover_izquierda(pos, mapa):
    fila, columna = pos
    if columna - 1 >= 0 and mapa[fila][columna - 1] != 1:
        return (fila, columna - 1)
    return None

def mover_arriba(pos, mapa):
    fila, columna = pos
    if fila - 1 >= 0 and mapa[fila-1][columna] != 1:
        return (fila - 1, columna)
    return None

def mover_abajo(pos, mapa):
    fila, columna = pos
    if fila + 1 < len(mapa) and mapa[fila+1][columna] != 1:
        return (fila + 1, columna)
    return None

def verificar_si_es_paquete(pos, posiciones):
    return pos in posiciones


pila = [nodo_inicial]
visitados = set()


def reconstruir_camino(nodo):
    """ Retrocede desde el nodo donde se encontró el paquete hasta el inicio. """
    camino = []
    while nodo.padre is not None:  # Hasta que lleguemos al nodo inicial
        camino.append(nodo.operador)
        nodo = nodo.padre
    return camino[::-1]  # Invertimos para mostrar desde el inicio hasta el paquete


def expandir_nodo():
    while pila:  
        nodo_actual = pila.pop(0)  

        if nodo_actual.estado in visitados:
            continue  
        
        visitados.add(nodo_actual.estado)

        if verificar_si_es_paquete(nodo_actual.estado, posicion_paquetes):
            print("Camino para llegar al paquete:", reconstruir_camino(nodo_actual))
            return  

        movimientos = [
            mover_derecha(nodo_actual.estado, mapa),
            mover_izquierda(nodo_actual.estado, mapa),
            mover_arriba(nodo_actual.estado, mapa),
            mover_abajo(nodo_actual.estado, mapa)
        ]

        for movimiento, operador in zip(movimientos, ["derecha", "izquierda", "arriba", "abajo"]):
            if movimiento is not None and movimiento not in visitados:
                nuevo_nodo = Nodo(movimiento, nodo_actual, operador, nodo_actual.profundidad + 1)
                pila.append(nuevo_nodo)

expandir_nodo()
