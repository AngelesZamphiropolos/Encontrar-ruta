import random

class Juego:
    def __init__(self, opcion: int):
        self.opcion = opcion
        self.filas = 5
        self.columnas = 9
        self.limite_escape = 20
        self.cant_escape = 0
        #Arriba, abajo, izquierda, derecha, este es de 8 mov [(-1,-1), (-1,0), (-1,1), (1,0), (1,-1), (1,1), (0,-1), (0,1)]
        self.movimientos = [(-1,-1), (-1,0), (-1,1), (1,0), (1,-1), (1,1), (0,-1), (0,1)]

        #inicializamos el laberinto
        self.laberinto = [[". " for _ in range(self.columnas)] for _ in range(self.filas)]

        # Posición inicial del personaje
        print(f"- Filas: 0 al {self.filas - 1}\n- Columnas: 0 al {self.columnas - 1}")
        pos_fila_usuario = input("Ingresa tu posición inicial:\n- Fila: ")
        pos_columna_usuario = input("- Columna: ")

        # Validamos que sea una posicion valida
        while (validar_numeros(pos_fila_usuario) == False  or validar_numeros(pos_columna_usuario) == False or int(pos_fila_usuario) < 0 or int(pos_fila_usuario) > self.filas - 1 or int(pos_columna_usuario) < 0 or int(pos_columna_usuario) > self.columnas - 1):
            print("Error, elija una opción válida...")
            pos_fila_usuario = input("Ingresa tu posición inicial:\n- Fila: ")
            pos_columna_usuario = input("- Columna: ")

        pos_fila_usuario = int(pos_fila_usuario)
        pos_columna_usuario = int(pos_columna_usuario)

        # Inicializar las posiciones según la opción
        if self.opcion == 1:
            self.gato = (pos_fila_usuario, pos_columna_usuario)
            # fila y columna del raton
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            # validamos que no aparezca en la misma posicion que el usuario
            if f != pos_fila_usuario or c != pos_columna_usuario:
                self.raton = (f, c)
        else:
            self.raton = (pos_fila_usuario, pos_columna_usuario)
            # fila y columna del gato
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            # validamos que no aparezca en la misma posicion que el usuario
            if f != pos_fila_usuario or c != pos_columna_usuario:
                self.gato = (f, c)
            
        #Agregamos a los personajes en el tablero
        fila, columna = self.gato
        self.laberinto[fila][columna] = "😼"

        fila, columna = self.raton
        self.laberinto[fila][columna] = "🐭"
        
    def imprimir_laberinto(self):
        # Imprimimos el laberinto
        for i in range(self.filas):
            for j in range (self.columnas):
                print(self.laberinto[i][j], end=" ")
            print("")
    
    def fin_programa(self):
        # Verifica si el gato atrapó al raton o si el ratón pudo escapar
        if self.gato == self.raton or self.cant_escape == self.limite_escape:
            return True
        return False
    
    def gato_gana(self, gato, raton):
        if gato == raton:
            return True
        return False
    
    def raton_gana(self, gato, raton):
        if gato != raton and self.cant_escape == self.limite_escape:
            return True
        return False
    
    def jugadas_validas(self, posicion, prohibida=None):
        # separamos la fila y columna de posicion
        fila, columna = posicion
        # creamos una lista de posiciones validas
        resultado = []
        # recorremos los movimientos que se puede hacer (arriba, abajo, izq, der, y las diagonales)
        for f, c in self.movimientos:
            f_final = fila + f
            c_final = columna + c
            # vemos si es posible hacer ese movimiento
            if 0 <= f_final < self.filas and 0 <= c_final < self.columnas:
                # para que no pueda moverse en la posicion anterior del usuario
                if prohibida is None or (f_final, c_final) != prohibida:
                    resultado.append((f_final, c_final))

        return resultado

    def distancia(self, p1, p2):
        # Distancia Manhattan
        return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
    
    def minimax_gato(self, gato , raton, nivel_profundidad, max_profundidad, turno_ia):
        #Cuando el gato le captura al raton
        if gato == raton:
            #para que el valor sea grande, y mientras menos profundidad, mas grande será el valor
            return (1000 - nivel_profundidad, gato, raton)
        
        # Cuando no le llega a capturar
        if nivel_profundidad == max_profundidad:
            # si la distancia es pequenha mejor para el gato entonces por eso usamos negativo, porque un numero chico negativo es mayor que un numero grande negativo
            return (-self.distancia(gato,raton), gato, raton)
    
        # Si es el turno de la ia
        if turno_ia:
            # le cargamos un numero muy chico ya que es el maximizador y buscará el valor mas alto posible
            mejor_valor = -10**9
            mejor_movimiento = None
            # recorre todos los movimientos posibles del gato
            for mov in self.jugadas_validas(gato):
                # usamos _ ya que ese valor de retorno no nos sirve
                valor, _, _ = self.minimax_gato(mov, raton, nivel_profundidad + 1, max_profundidad, not(turno_ia))
                # elegimos el maximo valor y capturamos esa posicion
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
        
        if nivel_profundidad == max_profundidad:
            return (self.distancia(gato,raton), gato, raton)
    
        #Si es el turno de la ia raton
        if turno_ia:
            #le cargamos un numero muy chico ya que es el maximizador y buscará el valor mas alto posible
            mejor_valor = -10**9
            mejor_movimiento = None

            for mov in self.jugadas_validas(raton, prohibida=gato_anterior):
                #usamos _ ya que ese valor de retorno no nos sirve
                valor, _, _ = self.minimax_raton(gato, mov, nivel_profundidad + 1, max_profundidad, not(turno_ia), gato_anterior)
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
                valor, _, _ = self.minimax_raton(mov, raton, nivel_profundidad + 1, max_profundidad, not(turno_ia), gato_anterior)
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
    # Selección de personaje
    opcion = input("Elija el personaje que desea ser: \n1. Gato\n2. Raton\nOpción: ")
    
    # validamos las opciones ingresadas
    while not (validar_numeros(opcion) and validar_opciones([1,2], opcion)):
        print("Error, elija una opción existente...")
        opcion = input("Elija el personaje que desea ser: \n1. Gato\n2. Raton\nOpción: ")

    opcion = int(opcion)

    #Creamos el objeto juego
    juego = Juego(opcion)

    # imprimimos el laberinto
    juego.imprimir_laberinto()

    while not juego.fin_programa():
        # Usuario es el GATO  
        if juego.opcion == 1:  
            fila, col = juego.gato
            
            mov = input("Moverse con:\n- W: arriba\n- S: abajo\n- A: izquierda\n- D: derecha\n- WA: Arriba Izquierda\n- WD: Arriba Derecha\n- SA: Abajo Izquierda\n- SD: Abajo Derecha\nOpcion: ")

            # validar opciones
            while mov.lower() not in ["w","s","a","d","wa","aw","wd","dw","sa","as","sd","ds"]:                
                print("Error, el movimiento no se pudo realizar...")
                mov = input("Moverse con:\n- W: arriba\n- S: abajo\n- A: izquierda\n- D: derecha\n- WA: Arriba Izquierda\n- WD: Arriba Derecha\n- SA: Abajo Izquierda\n- SD: Abajo Derecha\nOpcion: ")

            # Mover de lugar al usuario
            if mov.lower() == "w":
                nueva_fila = fila - 1
                nueva_col = col
            elif mov.lower() == "s":
                nueva_fila = fila + 1
                nueva_col = col
            elif mov.lower() == "a":
                nueva_fila = fila 
                nueva_col = col - 1
            elif mov.lower() == "d":
                nueva_fila = fila
                nueva_col = col + 1
            elif mov.lower() == "wa" or mov.lower() == "aw":
                nueva_fila = fila - 1
                nueva_col = col - 1
            elif mov.lower() == "wd" or mov.lower() == "dw":
                nueva_fila = fila - 1
                nueva_col = col + 1
            elif mov.lower() == "sa" or mov.lower() == "as":
                nueva_fila = fila + 1
                nueva_col = col - 1
            elif mov.lower() == "sd" or mov.lower() == "ds":
                nueva_fila = fila + 1
                nueva_col = col + 1

            # Guardar posición anterior del gato
            fila_ant_gato, col_ant_gato = juego.gato
            gato_anterior = (fila_ant_gato, col_ant_gato)

            # si la nueva posicion es valida, el personaje se mueve
            if (nueva_fila, nueva_col) in juego.jugadas_validas(juego.gato):
                juego.gato = (nueva_fila, nueva_col)
                juego.laberinto[fila][col] = ". "  # limpiar celda anterior
                juego.laberinto[nueva_fila][nueva_col] = "😼"

            # si no es valida , imprime este mensaje y le deja en su lugar
            else:
                print("Movimiento inválido, el gato se queda en su lugar.")
                juego.laberinto[fila][col] = "😼"

            
            #La ia es el RATON
            fila, col = juego.raton
            juego.laberinto[fila][col] = ". "
            _, _, nuevo_raton = juego.minimax_raton(juego.gato, juego.raton, 0, 4, True, gato_anterior)
            juego.raton = nuevo_raton
            fila, col = juego.raton
            juego.laberinto[fila][col] = "🐭"

            # indica que atrapo al raton
            if juego.raton == juego.gato:
                juego.laberinto[fila][col] = "💥" 
                break
            else:
                juego.laberinto[fila][col] = "🐭"
                fila_gato, col_gato = juego.gato
                juego.laberinto[fila_gato][col_gato] = "😼"

        elif juego.opcion == 2:  
            # Usuario es el RATÓN
            fila, col = juego.raton
            # limpiar celda anterior
            juego.laberinto[fila][col] = ". "  

            mov = input("Moverse con:\n- W: arriba\n- S: abajo\n- A: izquierda\n- D: derecha\nOpcion: ")
            
            # validar opciones
            while mov.lower() not in ["w","s","a","d","wa","aw","wd","dw","sa","as","sd","ds"]:                
                print("Error, el movimiento no se pudo realizar...")
                mov = input("Moverse con:\n- W: arriba\n- S: abajo\n- A: izquierda\n- D: derecha\n- WA: Arriba Izquierda\n- WD: Arriba Derecha\n- SA: Abajo Izquierda\n- SD: Abajo Derecha\nOpcion: ")

            # movimientos 
            if mov.lower() == "w":
                nueva_fila = fila - 1
                nueva_col = col
            elif mov.lower() == "s":
                nueva_fila = fila + 1
                nueva_col = col
            elif mov.lower() == "a":
                nueva_fila = fila 
                nueva_col = col - 1
            elif mov.lower() == "d":
                nueva_fila = fila
                nueva_col = col + 1
            elif mov.lower() == "wa" or mov.lower() == "aw":
                nueva_fila = fila - 1
                nueva_col = col - 1
            elif mov.lower() == "wd" or mov.lower() == "dw":
                nueva_fila = fila - 1
                nueva_col = col + 1
            elif mov.lower() == "sa" or mov.lower() == "as":
                nueva_fila = fila + 1
                nueva_col = col - 1
            elif mov.lower() == "sd" or mov.lower() == "ds":
                nueva_fila = fila + 1
                nueva_col = col + 1

            # si la nueva posicion es valida, el personaje se mueve
            if (nueva_fila, nueva_col) in juego.jugadas_validas(juego.raton):
                juego.raton = (nueva_fila, nueva_col)
                juego.laberinto[fila][col] = ". "
                juego.laberinto[nueva_fila][nueva_col] = "🐭"

             # si no es valida , imprime este mensaje y le deja en su lugar
            else:
                print("Movimiento inválido, el raton se queda en su lugar.")
                juego.laberinto[fila][col] = "🐭"


            if not juego.fin_programa():
                # La ia es el gato
                fila, col = juego.gato
                juego.laberinto[fila][col] = ". "
                _, nuevo_gato, _ = juego.minimax_gato(juego.gato, juego.raton, 0, 3, True)
                juego.gato = nuevo_gato
                fila, col = juego.gato
                juego.laberinto[fila][col] = "😼"

        
        # aumentar turnos de escape
        juego.cant_escape += 1

        # imprimir tablero
        juego.imprimir_laberinto()

    if opcion == 1:
        if juego.raton_gana(juego.gato, juego.raton):
            print("Perdiste... No pudiste atrapar al raton :(")
    else:
        if juego.raton_gana(juego.gato, juego.raton):
            print("GANASTE!! Pudiste escapar del gato")
        elif juego.gato_gana(juego.gato, juego.raton):
            juego.raton = "😼"
            print("Perdiste... No pudiste escapar del gato y te comió :(")

    opcion = input("Desea seguir jugando? (si, no): ")
    while opcion.lower() != "si" and opcion.lower() != "no":
        print("Opcion invalida...")
        opcion = input("Desea seguir jugando? (si, no): ")
    
    if (opcion.lower() == "no"):
        jugar = False
