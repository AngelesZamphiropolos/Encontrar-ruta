import random

class Juego:
    def __init__(self):
        #definir tamanho de filas y columnas
        self.filas = 5
        self.columnas = 9

        #definir el limite de movimientos para escapar o agarrar
        self.limite_escape = 15
        self.cant_escape = 0

        #Arriba, abajo, izquierda, derecha, este es de 8 mov [(-1,-1), (-1,0), (-1,1), (1,0), (1,-1), (1,1), (0,-1), (0,1)]
        self.movimientos = [(-1,0), (1,0), (0,-1), (0,1)]

        #inicializamos el laberinto
        self.laberinto = [[". " for _ in range(self.columnas)] for _ in range(self.filas)]

        
        #Posicion del gato
        pos_fila_gato = random.randint(0, self.filas - 1)
        pos_columna_gato = random.randint(0, self.columnas - 1)
        self.gato = (pos_fila_gato, pos_columna_gato)

        #Posicion del raton
        pos_fila_raton = random.randint(0, self.filas - 1)
        pos_columna_raton = random.randint(0, self.columnas - 1)

        #validamos que el raton no aparezca en la misma posicion que el gato
        while pos_fila_raton == pos_fila_gato and pos_columna_raton == pos_columna_gato:
            #Buscamos otra posicion para el raton
            pos_fila_raton = random.randint(0, self.filas - 1)
            pos_columna_raton = random.randint(0, self.columnas - 1)
        
        self.raton = (pos_fila_raton, pos_columna_raton)

        #Posicion del queso
        pos_fila_queso = random.randint(0, self.filas - 1)
        pos_columna_queso = random.randint(0, self.columnas - 1)

        #validamos que el queso no aparezca en la misma posicion que el gato ni el raton
        while pos_fila_queso == pos_fila_gato and pos_columna_queso == pos_columna_gato or pos_fila_raton == pos_fila_queso and pos_columna_raton == pos_columna_queso:
            #Buscamos otra posicion para el queso
            pos_fila_queso = random.randint(0, self.filas - 1)
            pos_columna_queso = random.randint(0, self.columnas - 1)
        
        self.queso = (pos_fila_queso, pos_columna_queso)

        #Agregamos a los personajes en el tablero
        fila, columna = self.gato
        self.laberinto[fila][columna] = "😼"

        fila, columna = self.raton
        self.laberinto[fila][columna] = "🐭"

        fila, columna = self.queso
        self.laberinto[fila][columna] = "🧀"
        
    def imprimir_laberinto(self):
        for i in range(self.filas):
            for j in range (self.columnas):
                print(self.laberinto[i][j], end=" ")
            print("")
    
    def fin_programa(self):
        if self.gato == self.raton or self.cant_escape == self.limite_escape:
            return True
        return False
    
    def gato_gana(self, gato, raton, queso):
        if gato == raton:
            return True
        return False
    
    def raton_gana(self, gato, raton):
        if gato != raton and self.cant_escape == self.limite_escape:
            return True
        return False
    
    def jugadas_validas(self, posicion, prohibida=None):
        #separamos la fila y columna de posicion
        fila, columna = posicion
        #creamos una lista de posiciones validas
        resultado = []
        #recorremos los movimientos que se puede hacer (arriba, abajo, izq, der)
        for f, c in self.movimientos:
            f_final, c_final = fila + f, columna + c
            #vemos si es posible hacer ese movimiento
            if 0 <= f_final < self.filas and 0 <= c_final < self.columnas:
                if prohibida is None or (f_final, c_final) != prohibida:
                    resultado.append((f_final, c_final))

        return resultado

    def distancia(self, p1, p2):
        #p1[0] ---> fila de p1
        #p1[1] ---> columna de p1
        #p2[0] ---> fila de p2
        #p2[1] ---> columna de p2

        return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

    def distancia_raton_queso(self, gato, raton):
        #Ver si conviene acercarse al queso y al gato
        distancia_gato = self.distancia(gato, raton)
        distancia_queso = self.distancia(raton, self.queso)

        # Pesa más acercarse al queso que alejarse del gato
        alejarse_gato = 1     
        acercarse_queso = 8

        #esto es si llega a agarrar el queso, entonces le da un puntaje extra
        if raton == self.queso:
            premio_queso = 100

        else: premio_queso = 0

        return alejarse_gato * distancia_gato - acercarse_queso * distancia_queso + premio_queso

    def minimax_gato(self, gato , raton, nivel_profundidad, max_profundidad, turno_ia):
        #Cuando el gato le captura al raton
        if gato == raton:
            #para que el valor sea grande, y mientras menos profundidas, mas grande sera el valor
            return (1000 - nivel_profundidad, gato, raton)
        
        #Cuando no le llega a capturar
        if nivel_profundidad == max_profundidad:
            #para minimizar la distancia entre el gato y el raton
            return (-self.distancia(gato,raton), gato, raton)
    
        #Si es el turno de la ia
        if turno_ia:
            #le cargamos un numero muy chico ya que es el maximizador y buscará el valor mas alto posible
            mejor_valor = -10**9
            mejor_movimiento = None
            #recorre todos los movimientos posibles del gato
            for mov in self.jugadas_validas(gato):
                #usamos _ ya que ese valor de retorno no nos sirve
                valor, _, _ = self.minimax_gato(mov, raton, nivel_profundidad + 1, max_profundidad, not(turno_ia))
                #elegimos el maximo valor y capturamos esa posicion
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov

            return (mejor_valor, mejor_movimiento, raton)
        
        #si es el turno del usuario
        else:
            mejor_valor = 10**9
            mejor_movimiento = None
            #recorre movimientos de raton
            for mov in self.jugadas_validas(raton):
                valor, _, _ = self.minimax_gato(gato, mov, nivel_profundidad + 1, max_profundidad, not(turno_ia))
                #busca el menor valor y se mueve a ese
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov
            return (mejor_valor, gato, mejor_movimiento)
        
    def minimax_raton(self, gato , raton, nivel_profundidad, max_profundidad, turno_ia, gato_anterior):
        # Calcular distancia de este estado 
        valor_actual = self.distancia_raton_queso(gato, raton)

        # Si el ratón ya llegó al queso → victoria inmediata
        if raton == self.queso:
            return (1000 - nivel_profundidad, gato, raton)
        
        if nivel_profundidad == max_profundidad:
            return (valor_actual, gato, raton)
        
        # Si el queso está en una de las 4 jugadas posibles del ratón, ir directo al queso
        if self.queso in self.jugadas_validas(raton, prohibida=gato_anterior):
            return (1000, gato, self.queso)
        
        #Si es el turno de la ia raton
        if turno_ia:
            #le cargamos un numero muy chico ya que es el maximizador y buscará el valor mas alto posible
            mejor_valor = -10**9
            mejor_movimiento = None

            for mov in self.jugadas_validas(raton, prohibida = gato_anterior):
                #usamos _ ya que ese valor de retorno no nos sirve
                valor, _, _ = self.minimax_raton(gato, mov, nivel_profundidad + 1, max_profundidad, not(turno_ia), gato)
                
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov

            return (mejor_valor, gato, mejor_movimiento)
        
        #si es el turno del usuario gato
        else:
            if gato == raton:
                return (-1000 + nivel_profundidad, gato, raton)
        
            mejor_valor = 10**9
            mejor_movimiento = None
            for mov in self.jugadas_validas(gato):
                valor, _, _ = self.minimax_raton(mov, raton, nivel_profundidad + 1, max_profundidad, not(turno_ia), gato)
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = mov
            return (mejor_valor, mejor_movimiento, raton)


def validar_numeros(num):
    try:
        int(num)
        return True
    except:
        print("Solo puedes ingresar números")
        return False

def validar_opciones(opciones, num):
    try:
        num = int(num)
        for opcion in opciones:
            if opcion == num:
                return True
    except:
        return False
   

jugar = True

while jugar:
    #Creamos el objeto juego
    juego = Juego()

    # Selección de personaje
    opcion = input("Elija el personaje que desea ser: \n1. Gato\n2. Raton\nOpción: ")
    
    while not (validar_numeros(opcion) and validar_opciones([1,2], opcion)):
        print("Error, elija una opción existente...")
        opcion = input("Elija el personaje que desea ser: \n1. Gato\n2. Raton\nOpción: ")

    opcion = int(opcion)
    if opcion == 1:
        print(f"Debes atrapar al raton antes de que realice {juego.limite_escape} movimientos.")
    else:
        print(f"Debes hacer {juego.limite_escape} movimientos sin que el gato te atrape y ganarás!!!")
    

    juego.imprimir_laberinto()

    while not juego.fin_programa():
        # La ia es el gato
        fila, col = juego.gato

        # Guardar posición anterior del gato
        gato_anterior = (fila, col)

        juego.laberinto[fila][col] = ". "
        _, nuevo_gato, _ = juego.minimax_gato(juego.gato, juego.raton, 0, 7, True)
        juego.gato = nuevo_gato
        fila, col = juego.gato
        juego.laberinto[fila][col] = "😼"

        print("-------------------------")
        #La ia es el RATON
        fila, col = juego.raton
        juego.laberinto[fila][col] = ". "
        _, _, nuevo_raton = juego.minimax_raton(juego.gato, juego.raton, 0, 7, True, gato_anterior)
        juego.raton = nuevo_raton
        fila, col = juego.raton
        juego.laberinto[fila][col] = "🐭"

        if juego.raton == juego.queso:
            juego.laberinto[fila][col] = "🐭"

        if juego.raton == juego.gato:
            juego.laberinto[fila][col] = "💥"  # 💥 indica que se atrapó al ratón
            break
        else:
            juego.laberinto[fila][col] = "🐭"
            fila_gato, col_gato = juego.gato
            juego.laberinto[fila_gato][col_gato] = "😼"

        
        # aumentar turnos de escape
        juego.cant_escape += 1

        # imprimir tablero
        juego.imprimir_laberinto()

    if opcion == 1:
        if juego.raton_gana(juego.gato, juego.raton):
            print("Perdiste... No pudiste atrapar al ratón :(")
        elif juego.gato_gana(juego.gato, juego.raton, juego.queso):
            print("GANASTE!! Pudiste atrapar al ratón :(")
    else:
        if juego.raton_gana(juego.gato, juego.raton):
            print("GANASTE!! Pudiste escapar del gato")
        elif juego.gato_gana(juego.gato, juego.raton, juego.queso):
            juego.raton = "😼"
            print("Perdiste... No pudiste escapar del gato y te comió :(")


    opcion = input("Desea seguir jugando? (si, no): ")
    while opcion.lower() != "si" and opcion.lower() != "no":
        print("Opcion invalida...")
        opcion = input("Desea seguir jugando? (si, no): ")
    
    if (opcion.lower() == "no"):
        jugar = False