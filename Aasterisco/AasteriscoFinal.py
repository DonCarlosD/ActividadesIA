import pygame
import heapq
import math

# Configuración de la ventana y el tamaño de la cuadrícula
ANCHO_VENTANA = 800  # Ancho de la ventana en píxeles
FILAS = 11  # Número de filas y columnas (cuadrícula de 11x11)
ANCHO_NODO = ANCHO_VENTANA // FILAS  # Tamaño de cada nodo en píxeles

# Definición de colores en formato RGB
BLANCO = (255, 255, 255)  # Espacio libre
NEGRO = (0, 0, 0)  # Paredes
GRIS = (200, 200, 200)  # Líneas de la cuadrícula
VERDE = (0, 255, 0)  # Nodo de inicio
ROJO = (255, 0, 0)  # Nodo de fin
AZUL = (0, 0, 255)  # Camino más corto
AMARILLO = (255, 255, 0)  # Nodos explorados
CYAN = (0, 255, 255)      # Nodo actual
NARANJA = (255, 165, 0)   # Nodos en open set

# Inicializar Pygame
pygame.init()
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))  # Crear ventana
pygame.display.set_caption("A* - Exploración consistente")  # Título de la ventana
clock = pygame.time.Clock()  # Reloj para controlar la velocidad de fotogramas

# Clase Nodo que representa cada celda de la cuadrícula
class Nodo:
    def __init__(self, fila, col):
        self.fila = fila  # Fila en la cuadrícula
        self.col = col  # Columna en la cuadrícula
        self.x = self.col * ANCHO_NODO  # Posición x en píxeles
        self.y = self.fila * ANCHO_NODO  # Posición y en píxeles
        self.color = BLANCO  # Color inicial (espacio libre)
        self.vecinos = []  # Lista de nodos vecinos accesibles
        self.g = float('inf')  # Costo acumulado desde el inicio
        self.f = float('inf')  # Costo total estimado (g + heurística)
        self.padre = None  # Nodo previo en el camino
        self.explorado = False  # Si el nodo ha sido explorado

    def es_pared(self):
        return self.color == NEGRO  # Devuelve True si el nodo es una pared

    def hacer_inicio(self):
        self.color = VERDE  # Marca el nodo como inicio (color verde)

    def hacer_fin(self):
        self.color = ROJO  # Marca el nodo como fin (color rojo)

    def hacer_pared(self):
        self.color = NEGRO  # Marca el nodo como pared (color negro)

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, ANCHO_NODO, ANCHO_NODO))
    
    def __lt__(self, other): 
        if self.f == other.f:
            # Desempate basado en la posición (prioriza nodos con menor fila o columna)
            return (self.fila + self.col) < (other.fila + other.col)
        return self.f < other.f

    def dibujar_info(self, ventana, font, end):
        g_text = font.render(f"g:{int(self.g) if self.g != float('inf') else '-'}", True, (0,0,0))
        h_text = font.render(f"h:{int(heuristica(self, end)) if end else '-'}", True, (0,0,0))
        f_text = font.render(f"f:{int(self.f) if self.f != float('inf') else '-'}", True, (0,0,0))
        padre_text = font.render(f"P:{self.padre.fila},{self.padre.col}" if self.padre else "P:-", True, (0,0,0))
        ventana.blit(g_text, (self.x+2, self.y+2))
        ventana.blit(h_text, (self.x+2, self.y+15))
        ventana.blit(f_text, (self.x+2, self.y+28))
        ventana.blit(padre_text, (self.x+2, self.y+41))

# Crea la cuadrícula de nodos
def crear_grid(filas):
    grid = []
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j)  # Crea un nodo en la posición (i, j)
            grid[i].append(nodo)
    return grid

# Dibuja las líneas de la cuadrícula
def dibujar_grid(ventana, filas):
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ANCHO_NODO), (ANCHO_VENTANA, i * ANCHO_NODO))  # Líneas horizontales
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ANCHO_NODO, 0), (j * ANCHO_NODO, ANCHO_VENTANA))  # Líneas verticales

# Dibuja la cuadrícula completa con los nodos
def dibujar(ventana, grid, filas, font, end):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
            nodo.dibujar_info(ventana, font, end)
    dibujar_grid(ventana, filas)
    pygame.display.update()

# Obtiene la posición de un clic del mouse y la convierte en coordenadas de la cuadrícula
def obtener_click_pos(pos, filas):
    x, y = pos
    col = x // ANCHO_NODO  # Calcula la columna en la cuadrícula
    fila = y // ANCHO_NODO  # Calcula la fila en la cuadrícula
    return fila, col

# Conecta los nodos vecinos (incluyendo diagonales)
def conectar_vecinos(grid, filas):
    for fila in grid:
        for nodo in fila:
            nodo.vecinos = []
            if nodo.es_pared():
                continue

            direcciones = [
                (-1, 0, False), (1, 0, False), (0, -1, False), (0, 1, False),  # Cardinales
                (-1, -1, True), (-1, 1, True), (1, -1, True), (1, 1, True)     # Diagonales
            ]

            for dx, dy, diagonal in direcciones:
                nx, ny = nodo.fila + dx, nodo.col + dy
                if 0 <= nx < filas and 0 <= ny < filas:
                    vecino = grid[nx][ny]
                    if vecino.es_pared():
                        continue
                    if diagonal:
                        # Solo bloquear si ambos adyacentes cardinales son pared
                        adyacentes = []
                        ady1_f, ady1_c = nodo.fila, nodo.col + dy
                        if 0 <= ady1_f < filas and 0 <= ady1_c < filas:
                            adyacentes.append(grid[ady1_f][ady1_c].es_pared())
                        else:
                            adyacentes.append(False)
                        ady2_f, ady2_c = nodo.fila + dx, nodo.col
                        if 0 <= ady2_f < filas and 0 <= ady2_c < filas:
                            adyacentes.append(grid[ady2_f][ady2_c].es_pared())
                        else:
                            adyacentes.append(False)
                        # Solo bloquear si ambos son pared
                        if all(adyacentes):
                            continue
                    nodo.vecinos.append(vecino)

# Función heurística: distancia de Chebyshev (adecuada para diagonales)
def heuristica(nodo1, nodo2):
    dx = abs(nodo1.fila - nodo2.fila)
    dy = abs(nodo1.col - nodo2.col)
    return (dx + dy)*10

# Algoritmo A* para encontrar el camino óptimo
def a_estrella(start, end, grid):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (start.f, 0, start))
    start.g = 0
    start.f = heuristica(start, end)
    counter = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []

        current = heapq.heappop(open_set)[2]
        closed_set.add(current)
        current.explorado = True

        # Imprime información del nodo actual
        print(f"Nodo actual: ({current.fila},{current.col}) g={current.g:.2f} h={heuristica(current, end)} f={current.f:.2f} padre={f'({current.padre.fila},{current.col})' if current.padre else '-'}")

        if current == end:
            print("Camino encontrado.")
            camino = reconstruir_camino(end)
            print("Camino final:")
            for nodo in camino:
                print(f"({nodo.fila},{nodo.col})", end=" -> ")
            print()
            return camino

        for vecino in current.vecinos:
            dx = abs(vecino.fila - current.fila)
            dy = abs(vecino.col - current.col)
            if dx + dy == 1:
                costo_movimiento = 10
            else:
                costo_movimiento = 14
            
            tentative_g = current.g + costo_movimiento

            if tentative_g < vecino.g:
                vecino.padre = current
                vecino.g = tentative_g
                vecino.f = tentative_g + heuristica(vecino, end)
                if not any(vecino == item[2] for item in open_set):
                    counter += 1
                    heapq.heappush(open_set, (vecino.f, counter, vecino))

        # Imprime listas abierta y cerrada
        print("Lista abierta:", [(n[2].fila, n[2].col) for n in open_set])
        print("Lista cerrada:", [(nodo.fila, nodo.col) for nodo in closed_set])

        # Colorea todos los nodos en open_set como NARANJA (excepto start, end y el actual)
        for _, _, nodo in open_set:
            if nodo != start and nodo != end and nodo != current and not nodo.explorado:
                nodo.color = NARANJA

        # Visualización
        dibujar(VENTANA, grid, FILAS, pygame.font.SysFont("Arial", 12), end)
        for fila in grid:
            for nodo in fila:
                if nodo.explorado and nodo != start and nodo != end:
                    nodo.color = AMARILLO
        start.dibujar(VENTANA)
        end.dibujar(VENTANA)
        pygame.display.update()
        clock.tick(30)

    print("No se encontró camino.")
    return []

# Algoritmo A* paso a paso
def a_estrella_paso_a_paso(start, end, grid):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (start.f, 0, start))
    start.g = 0
    start.f = heuristica(start, end)
    counter = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Colorea todos los nodos en open_set como NARANJA (excepto start, end y el actual)
        for _, _, nodo in open_set:
            if nodo != start and nodo != end and nodo != current and not nodo.explorado:
                nodo.color = NARANJA

        # Colorea todos los nodos explorados como AMARILLO (excepto start y end)
        for fila in grid:
            for nodo in fila:
                if nodo.explorado and nodo != start and nodo != end:
                    nodo.color = AMARILLO

        current = heapq.heappop(open_set)[2]
        closed_set.add(current)
        current.explorado = True

        # Colorea el nodo actual como CYAN (excepto start y end)
        if current != start and current != end:
            current.color = CYAN

        if current == end:
            reconstruir_camino(end)
            yield True  # Camino encontrado
            return

        for vecino in current.vecinos:
            dx = abs(vecino.fila - current.fila)
            dy = abs(vecino.col - current.col)
            if dx + dy == 1:
                costo_movimiento = 10
            else:
                costo_movimiento = 14

            tentative_g = current.g + costo_movimiento

            if tentative_g < vecino.g:
                vecino.padre = current
                vecino.g = tentative_g
                vecino.f = tentative_g + heuristica(vecino, end)
                if not any(vecino == item[2] for item in open_set):
                    counter += 1
                    heapq.heappush(open_set, (vecino.f, counter, vecino))

        # Visualización
        dibujar(VENTANA, grid, FILAS, pygame.font.SysFont("Arial", 12), end)
        yield False  # Un paso realizado

    yield None  # No se encontró camino

# Reconstruye el camino encontrado por A*
def reconstruir_camino(end):
    camino = []
    current = end
    while current.padre:  # Recorre los nodos padres desde el fin hasta el inicio
        camino.append(current)
        current = current.padre
    camino.reverse()  # Invierte el camino para que vaya de inicio a fin
    for nodo in camino:
        nodo.color = AZUL  # Colorea el camino de azul
    pygame.display.update()  # Actualiza la pantalla
    return camino

# Función principal del programa
def main():
    grid = crear_grid(FILAS)
    start = None
    end = None
    running = True
    solving = False
    paso_a_paso = None
    font = pygame.font.SysFont("Arial", 12)

    while running:
        dibujar(VENTANA, grid, FILAS, font, end)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si el usuario cierra la ventana
                running = False

            if pygame.mouse.get_pressed()[0] and not solving:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS)  # Obtiene la posición del clic
                clicked_node = grid[fila][col]  # Nodo clickeado
                if not start and clicked_node != end:  # Si no hay inicio, establece el inicio
                    start = clicked_node
                    start.hacer_inicio()
                elif not end and clicked_node != start:  # Si no hay fin, establece el fin
                    end = clicked_node
                    end.hacer_fin()
                elif clicked_node != start and clicked_node != end:  # Si no es inicio ni fin, establece una pared
                    clicked_node.hacer_pared()

            if pygame.mouse.get_pressed()[2] and not solving:  # Clic derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS)  # Obtiene la posición del clic
                clicked_node = grid[fila][col]  # Nodo clickeado
                if clicked_node == start:  # Si es el inicio, lo elimina
                    start.color = BLANCO  # Restablece el color
                    start = None  # Restablece la variable start
                elif clicked_node == end:  # Si es el fin, lo elimina
                    end.color = BLANCO  # Restablece el color
                    end = None  # Restablece la variable end
                elif clicked_node.es_pared():  # Si es una pared, la elimina
                    clicked_node.color = BLANCO  # Restablece el color

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not solving:
                    conectar_vecinos(grid, FILAS)
                    solving = True
                    a_estrella(start, end, grid)
                    solving = False
                if event.key == pygame.K_n and solving and paso_a_paso:
                    try:
                        resultado = next(paso_a_paso)
                        if resultado is not False:
                            solving = False  # Termina si encuentra camino o no hay más pasos
                    except StopIteration:
                        solving = False

    pygame.quit()  # Cierra Pygame

if __name__ == "__main__":
    main()  # Ejecuta la función principal