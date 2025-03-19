import heapq  # Librería para la cola de prioridad

posicion_paquetes = []  # Lista con las posiciones de los paquetes
cola_prioridad = []  # Cola de prioridad (heap)

class Nodo:
    def __init__(self, estado, padre=None, operador=None, profundidad=0, costo=0):
        self.estado = estado  # Posición en la matriz (fila, columna)
        self.padre = padre  # Referencia al nodo padre
        self.operador = operador  # Movimiento realizado para llegar aquí
        self.profundidad = profundidad  # Nivel en el árbol de búsqueda
        self.costo = costo  # Costo acumulado para llegar aquí

    def __lt__(self, otro): #funcion para indicarle al heap que compare los nodos por costo y le de prioridad al menor costo
        return self.costo < otro.costo  # Compara nodos por costo para la cola de prioridad

    def __str__(self): #funcion para imprimir el nodo
        return f"Nodo(estado={self.estado}, operador={self.operador}, profundidad={self.profundidad}, costo={self.costo})"

def leer_mapa(archivo_txt):  # Función para leer el archivo de texto
    with open("archivo.txt", "r") as archivo:  # Se abre el archivo en modo lectura
        matriz = [list(map(int, linea.split())) for linea in archivo]  #Con el for recorremos todas las lineas, el split lo separa por espacios, el int los trabaja como numeros, el map los mapea y el list los deja como listas
    return matriz 

mapa = leer_mapa("archivo.txt")  

def es_campo_magnetico(pos, mapa): # Funcion para verificar si la posicion es un campo magnetico
    fila, columna = pos
    return mapa[fila][columna] == 3

def encontrar_paquetes(mapa):   #Funcion para encontrar la posicion de los paquetes
    paquetes = []  
    for i, fila in enumerate(mapa):  #Recorremos las filas
        for j, valor in enumerate(fila):  #Recorremos las columnas
            if valor == 4:  
                paquetes.append((i, j))  
    return paquetes 

posicion_paquetes = encontrar_paquetes(mapa) # Asignamos los paquetes a posicion_paquetes

def encontrar_posicion_inicial(mapa):  #Funcion para encontrar la posicion inicial del nodo 
    for i, fila in enumerate(mapa):  #Recorremos las filas
        for j, valor in enumerate(fila):  #Recorremos las columnas
            if valor == 2:  
                return (i, j)  
    return None  

posicion_inicial = encontrar_posicion_inicial(mapa)  #Le asignamos la posicion inicial de nodo a posicion_inicial
nodo_inicial = Nodo(posicion_inicial, None, None, 0, 0)  # Creamos el primer nodo con la posicion inicial y costo 0

def mover_derecha(pos, mapa):  #Funcion para mover a la derecha
    fila, columna = pos
    if columna + 1 < len(mapa[0]) and mapa[fila][columna + 1] != 1:  
        return (fila, columna + 1)
    return None

def mover_izquierda(pos, mapa):  #Funcion para mover a la izquierda
    fila, columna = pos
    if columna - 1 >= 0 and mapa[fila][columna - 1] != 1:  
        return (fila, columna - 1)
    return None

def mover_arriba(pos, mapa):  #Funcion para mover hacia arriba
    fila, columna = pos
    if fila - 1 >= 0 and mapa[fila - 1][columna] != 1:  
        return (fila - 1, columna)
    return None

def mover_abajo(pos, mapa):  #Funcion para mover hacia abajo
    fila, columna = pos
    if fila + 1 < len(mapa) and mapa[fila + 1][columna] != 1:  
        return (fila + 1, columna)
    return None

def verificar_si_es_paquete(pos, posiciones):  #Funcion para verificar si la posicion es un paquete
    return pos in posiciones  

def costo_movimiento():  #Funcion para asignar el costo al movimiento
    return 1  

def costo_campo_magnetico():  #Funcion para asignar el costo al campo magnetico
    return 8


heapq.heappush(cola_prioridad, nodo_inicial)  # Se agrega el nodo inicial, recibe la cola de prioridad y el nodo inicial, este metodo heappush verifica que la cola de prioridad siempre este ordenada por costo usando la funcion definida la clase Nodo

visitados = set()  # Conjunto para almacenar nodos visitados

def reconstruir_camino(nodo):  #Funcion para recontruir el camino desde la meta hacia el padre una vez se haya encontrado el paquete
    camino = []  
    while nodo.padre is not None:  
        camino.append(nodo.operador)  
        nodo = nodo.padre  
    return camino[::-1]  # Se invierte la lista para mostrar el camino correcto

def costo_uniforme():  
    while cola_prioridad:  
        nodo_actual = heapq.heappop(cola_prioridad)  # Extrae el nodo con menor costo

        if nodo_actual.estado in visitados:  # Si ya lo visitamos, lo ignoramos
            continue  

        visitados.add(nodo_actual.estado)  # Marcamos el nodo como visitado

        if verificar_si_es_paquete(nodo_actual.estado, posicion_paquetes):  
            print("Camino encontrado:", reconstruir_camino(nodo_actual), "Costo:", nodo_actual.costo)  
            return  

        # Expansión de nodos con los movimientos posibles
        movimientos = [
            (mover_derecha(nodo_actual.estado, mapa), "derecha"),
            (mover_izquierda(nodo_actual.estado, mapa), "izquierda"),
            (mover_arriba(nodo_actual.estado, mapa), "arriba"),
            (mover_abajo(nodo_actual.estado, mapa), "abajo"),
        ]

        for posicion_nueva, operador in movimientos:
            if posicion_nueva is not None and posicion_nueva not in visitados: 
                if es_campo_magnetico(posicion_nueva, mapa): #Verificar si la posicion a donde nos moveriamos es un campo magnetico
                    nuevo_costo = nodo_actual.costo + costo_campo_magnetico() 
                    nuevo_nodo = Nodo(posicion_nueva, nodo_actual, operador, nodo_actual.profundidad + 1, nuevo_costo)  
                    heapq.heappush(cola_prioridad, nuevo_nodo) 
                else:
                    nuevo_costo = nodo_actual.costo + costo_movimiento()  # Costo acumulado
                    nuevo_nodo = Nodo(posicion_nueva, nodo_actual, operador, nodo_actual.profundidad + 1, nuevo_costo)  
                    heapq.heappush(cola_prioridad, nuevo_nodo)  # Se agrega el nodo con su costo

costo_uniforme()  # Ejecutar el algoritmo
