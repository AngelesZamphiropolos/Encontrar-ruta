#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <windows.h>

// Estructura para posiciones
typedef struct{
    int f, c;
} Pos;

// Símbolos
char *pared = "🔳";
char *camino = "  ";
char *inicio = "🟩";
char *fin = "🟩";
char *explorar = "▫️ ";
char *ruta = "🔹";

// Función para mover el cursor en la consola
void moverCursor(int x, int y){
    COORD coord = {x, y};
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

// Genera el laberinto con backtracking
void backtracking(int F, int C, char *lab[F][C], int f, int c){
    // Movimientos
    int movFila[] = {-2, 2, 0, 0};
    int movCol[] = {0, 0, -2, 2};
    int indices[4] = {0, 1, 2, 3};

    // Mezclar direcciones
    for (int i = 3; i > 0; i--){
        int j = rand() % (i + 1);
        int temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }

    // Movimientos posibles
    for (int i = 0; i < 4; i++){
        int indice = indices[i];
        int nueva_f = f + movFila[indice];
        int nueva_c = c + movCol[indice];

        // Verificar si no sale del rango
        if (nueva_f > 0 && nueva_f < F - 1 && nueva_c > 0 && nueva_c < C && strcmp(lab[nueva_f][nueva_c], pared) == 0){

            lab[f + movFila[indice] / 2][c + movCol[indice] / 2] = camino;
            lab[nueva_f][nueva_c] = camino;

            backtracking(F, C, lab, nueva_f, nueva_c);
        }
    }
}

// Imprimir el laberinto usando buffer para animación suave
void imprimir_laberinto(int F, int C, char *lab[F][C], char *buffer[F][C]){
    // Volver al inicio de la consola
    moverCursor(0, 1);

    for (int i = 0; i < F; i++){
        for (int j = 0; j < C; j++){
            // Solo imprimimos si hay cambio respecto al buffer
            if (strcmp(lab[i][j], buffer[i][j]) != 0){
                printf("%s", lab[i][j]);
                // Actualizamos buffer
                buffer[i][j] = lab[i][j];
            }
            else {
                printf("%s", lab[i][j]);
            }
        }
        printf("\n");
    }
    // Pausa para animación
    usleep(50000);
}

// BFS para resolver laberinto
void bfs(int F, int C, int inicio_f, int inicio_c, int fin_f, int fin_c, char *lab[F][C], char *buffer[F][C]){
    // Movimientos posibles
    int movFila[] = {-1, 1, 0, 0};
    int movCol[] = {0, 0, -1, 1};

    // Matriz visitado
    int visitado[F][C];

    // Matriz padre
    Pos padre[F][C];

    // Crear cola
    Pos cola[F * C];
    int frente = 0, final = 0;

    // Inicializar
    for (int i = 0; i < F; i++){
        for (int j = 0; j < C; j++){
            visitado[i][j] = 0;
            padre[i][j].f = -1;
            padre[i][j].c = -1;
        }
    }

    // Agregar la pos inicial a la cola
    cola[final++] = (Pos){inicio_f, inicio_c};

    // Marcar como visitado
    visitado[inicio_f][inicio_c] = 1;

    while (frente < final){
        // Sacar elemento de la cola
        Pos actual = cola[frente++];

        if (strcmp(lab[actual.f][actual.c], inicio) != 0 && strcmp(lab[actual.f][actual.c], fin) != 0){
            lab[actual.f][actual.c] = explorar;
        }

        imprimir_laberinto(F, C, lab, buffer);

        if (actual.f == fin_f && actual.c == fin_c) break;

        for (int i = 0; i < 4; i++){
            int nueva_f = actual.f + movFila[i];
            int nueva_c = actual.c + movCol[i];

            if (nueva_f >= 0 && nueva_f < F && nueva_c >= 0 && nueva_c < C && (strcmp(lab[nueva_f][nueva_c], camino) == 0 ||
                strcmp(lab[nueva_f][nueva_c], fin) == 0 || strcmp(lab[nueva_f][nueva_c], inicio) == 0) &&
                visitado[nueva_f][nueva_c] == 0){

                cola[final++] = (Pos){nueva_f, nueva_c};
                visitado[nueva_f][nueva_c] = 1;
                padre[nueva_f][nueva_c] = actual;
            }
        }
    }

    // Reconstruir camino
    Pos p = {fin_f, fin_c};
    while (!(p.f == -1 && p.c == -1)){
        if (strcmp(lab[p.f][p.c], fin) != 0){
            lab[p.f][p.c] = ruta;
        }
        p = padre[p.f][p.c];
    }
    lab[inicio_f][inicio_c] = inicio;
}

int main(){
    clock_t inicio_tiempo, fin_tiempo;
    double tiempo;

    // Guardamos el tiempo de inicio
    inicio_tiempo = clock();

    SetConsoleOutputCP(CP_UTF8);
    system("cls");

    // Para que no genere la misma secuencia de numeros
    srand(time(NULL));

    // Generar dimensiones
    int F = (rand() % (20 - 10 + 1)) + 10;
    int C = (rand() % (30 - 10 + 1)) + 10;

    // Si es par le agregamos 1
    if (F % 2 == 0){
        F++;
    }
    if (C % 2 == 0){
        C++;
    }

    // Generar la matriz
    char *lab[F][C];

    // Usar buffer para animación suave
    char *buffer[F][C];

    // Inicializar laberinto y buffer
    for (int i = 0; i < F; i++){
        for (int j = 0; j < C; j++){
            lab[i][j] = pared;
            // buffer vacío al inicio
            buffer[i][j] = "";
        }
    }

    lab[1][1] = camino;
    backtracking(F, C, lab, 1, 1);

    // Romper paredes al azar
    for (int i = 0; i < C; i++){
        // para que no rompa los bordes
        int f = rand() % (F - 2) + 1;
        int c = rand() % (C - 2) + 1;

        // Solo romper si es pared y hay caminos a ambos lados
        if (strcmp(lab[f][c], pared) == 0){
            if ((strcmp(lab[f - 1][c], camino) == 0 && strcmp(lab[f + 1][c], camino) == 0) ||
                (strcmp(lab[f][c - 1], camino) == 0 && strcmp(lab[f][c + 1], camino) == 0)){
                // Romper pared
                lab[f][c] = camino;
            }
        }
    }

    // Marcar inicio y fin
    lab[1][0] = inicio;
    lab[F - 1][C - 2] = fin;

    // Marcar como camino una celda al lado de inicio y del fin para que siempre se conecten
    lab[1][1] = camino;
    lab[F - 2][C - 2] = camino;

    bfs(F, C, 1, 0, F - 2, C - 2, lab, buffer);

    imprimir_laberinto(F, C, lab, buffer);

    // Guardamos el tiempo de fin
    fin_tiempo = clock();

    // Calculamos el tiempo en segundos
    tiempo = (double)(fin_tiempo - inicio_tiempo) / CLOCKS_PER_SEC;

    printf("Tiempo de ejecucion: %.2f segundos\n", tiempo);

    return 0;
}
