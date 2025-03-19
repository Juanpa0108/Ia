posicion_paquetes = [] #Arreglo que guarda la posicion de los paquetes

class Nodo: #Definicion de la clase Nodo, la cual guarda la estructura basica de un nodo
    def __init__(self, estado, padre=None, operador=None, profundidad=0):
        self.estado = estado  
        self.padre = padre  
        self.operador = operador  
        self.profundidad = profundidad 

    def __str__(self):
        return f"Nodo(estado={self.estado}, operador={self.operador}, profundidad={self.profundidad})"


def leer_mapa(archivo_txt): #Funcion para leer el archivo.txt y lo guardemos en una matriz
    with open("archivo.txt", "r") as archivo: #Abrimos el archivo en modo lectura
        matriz = [list(map(int, linea.split())) for linea in archivo] #Con el for recorremos todas las lineas, el split lo separa por espacios, el int los trabaja como numeros, el map los mapea y el list los deja como listas 
    return matriz

mapa = leer_mapa("archivo.txt") #Creamos la variable mapa la cual va a guardar la matriz que representa el mapa

def encontrar_paquetes(mapa): #Funcion para encontrar los paquetes
    paquetes = []  
    for i, fila in enumerate(mapa): #Recorremos filas
        for j, valor in enumerate(fila): #Recorremos columnas
            if valor == 4:  #Si la posicion es 4 se guarda en la variable local llamada paquetes
                paquetes.append((i, j))  
    return paquetes 

posicion_paquetes = encontrar_paquetes(mapa) #LLenamos la lista de los paquetes con la funcion creada previamente

def encontrar_posicion_inicial(mapa): #Funcion para encontrar la posicion inicial del "jugador"
    for i, fila in enumerate(mapa):  
        for j, valor in enumerate(fila):  
            if valor == 2:  
                return (i, j)  
    return None 

posicion_inicial = encontrar_posicion_inicial(mapa) #Creamos una variable llamada posicion_inicial y le asignamos el valor que nos retorne la funcion
nodo_inicial = Nodo(posicion_inicial, None, None, 0) #Creamos el nodo inicial con la posicion inicial del arbol, sin padre, sin movimientos y en profundidad 0

def mover_derecha(pos, mapa): #Funcion para moverse a la derecha
    fila, columna = pos
    if columna + 1 < len(mapa[0]) and mapa[fila][columna + 1] != 1: #Verficamos si con el movimiento nos salimos del mapa o colisionamos con alguna estructura
        return (fila, columna + 1)
    return None

def mover_izquierda(pos, mapa): #Funcion para moverse a la izquierda
    fila, columna = pos
    if columna - 1 >= 0 and mapa[fila][columna - 1] != 1: #Verficamos si con el movimiento nos salimos del mapa o colisionamos con alguna estructura
        return (fila, columna - 1)
    return None

def mover_arriba(pos, mapa): #Funcion para moverse hacia arriba
    fila, columna = pos
    if fila - 1 >= 0 and mapa[fila-1][columna] != 1: #Verficamos si con el movimiento nos salimos del mapa o colisionamos con alguna estructura
        return (fila - 1, columna)
    return None

def mover_abajo(pos, mapa): #Funcion para moverse hacia abajo
    fila, columna = pos
    if fila + 1 < len(mapa) and mapa[fila+1][columna] != 1: #Verficamos si con el movimiento nos salimos del mapa o colisionamos con alguna estructura
        return (fila + 1, columna)
    return None

def verificar_si_es_paquete(pos, posiciones): #Funcion para verificar si la posicion donde estamos es un paquete
    return pos in posiciones


pila = [nodo_inicial] #Creamos la pila con el nodo inicial
visitados = set() #Creamos un set de valores para almacenar los nodos que hemos visitado (para evitar ciclos)


def reconstruir_camino(nodo): #Funcion para reconstruir el camino desde la meta hacia el padre una vez se haya encontrado el paquete
    camino = []
    while nodo.padre is not None: #Se ejecuta hasta que el padre del Nodo sea None
        camino.append(nodo.operador)
        nodo = nodo.padre #Asigno el nodo padre a nodo para evaluarse en la proxima iteracion
    return camino[:: -1]  #Invertimos el camino que nos tomo llegar a la meta y lo devolvemos 


def expandir_nodo(): #Funcion principal
    while pila:  #Mientras existan elementos dentro de la pila
        nodo_actual = pila.pop(0)  #El nodo que se va a usar será la cabeza de la pila y se sacara

        if nodo_actual.estado in visitados: #Si el nodo actual ya fue visitado, no volveremos a el, continuamos la ejecucion
            continue  
        
        visitados.add(nodo_actual.estado) #Agregamos el nodo a visitados

        if verificar_si_es_paquete(nodo_actual.estado, posicion_paquetes): #Condicion para verificar si la posicion del nodo es un paquete 
            print("Camino para llegar al paquete:", reconstruir_camino(nodo_actual), " en la profundidad: ", nodo_actual.profundidad) #En caso de ser paquete se imprime en pantalla el camino para llegar hasta ahí y la profundidad
            return  

        movimientos = [ #Lista con los posibles movimientos
            mover_derecha(nodo_actual.estado, mapa),
            mover_izquierda(nodo_actual.estado, mapa),
            mover_arriba(nodo_actual.estado, mapa),
            mover_abajo(nodo_actual.estado, mapa)
        ]

        for movimiento, operador in zip(movimientos, ["derecha", "izquierda", "arriba", "abajo"]): #Le ponemos los nombres a las operaciones 
            if movimiento is not None and movimiento not in visitados: #Si el movimiento es valido y el la casilla hacia donde se va a mover no ha sido visitada, entra en la condicion
                nuevo_nodo = Nodo(movimiento, nodo_actual, operador, nodo_actual.profundidad + 1) #Creamos un nuevo nodo con la casilla donde se va a mover, como padre el nodo actual,  el operador que se uso para llegar hasta ahí y la profundidad que llevaba el nodo + 1
                pila.append(nuevo_nodo) #Se ingresa el nuevo nodo al final de la pila

expandir_nodo() #Llamado a la funcion
