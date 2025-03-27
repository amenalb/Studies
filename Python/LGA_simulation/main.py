import pygame
import random
import sys
# Ustawienia symulacji
WIDTH, HEIGHT = 600, 600  # Rozmiar okna
CELL_SIZE = 7            # Rozmiar komórki
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Kolory
BACKGROUND_COLOR = (0, 0, 0)
PARTICLE_COLOR = (0, 255, 0)
BARRIER_COLOR = (255, 0, 0)

# Kierunki (góra, prawo, dół, lewo)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Liczba cząstek do umieszczenia
try:
    PARTICLE_COUNT = int(input("Podaj liczbę cząstek do rozmieszczenia: "))
    if PARTICLE_COUNT < 1:
        raise ValueError("Liczba cząstek musi być większa od 0.")
except ValueError as e:
    print(f"Błąd: {e}")
    sys.exit(1)
#PARTICLE_COUNT = 7000  # Zmień na dowolną wartość

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacja LGA")
clock = pygame.time.Clock()

# Inicjalizacja siatki i bariery
def initialize_grid():
    grid = [[[] for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    barrier = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Tworzenie  bariery
    barrier_x = GRID_WIDTH // 4
    for y in range(GRID_HEIGHT):
        barrier[y][barrier_x] = True

    # Rozmieszczenie cząstek losowo
    for _ in range(PARTICLE_COUNT):
        x = random.randint(0, GRID_WIDTH // 4 - 1)  # 1/4 ekranu
        y = random.randint(0, GRID_HEIGHT - 1)      # Losowy wiersz
        direction = random.choice(range(4))         # Losowy kierunek (0, 1, 2, 3)
        grid[y][x].append(direction)                # Dodanie cząstki do komórki

    return grid, barrier

# Rysowanie cząstek i bariery
def draw_particles_and_barrier(grid, barrier):
    screen.fill(BACKGROUND_COLOR)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            # Rysowanie bariery
            if barrier[y][x]:
                pygame.draw.rect(screen, BARRIER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Rysowanie cząstek
            for direction in grid[y][x]:
                cx, cy = x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2
                dx, dy = DIRECTIONS[direction]
                px, py = cx + dx * (CELL_SIZE // 3), cy + dy * (CELL_SIZE // 3)
                pygame.draw.circle(screen, PARTICLE_COLOR, (px, py), 3)

# Usuwanie fragmentu bariery po kliknięciu
def remove_barrier(barrier, pos):
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        barrier[y][x] = False


def streaming(grid, barrier):
    new_grid = [[[] for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            for direction in grid[y][x]:
                dx, dy = DIRECTIONS[direction]
                nx, ny = x + dx, y + dy

                # Odbicie od brzegów
                if nx < 0 or nx >= GRID_WIDTH:
                    nx = x
                    direction = 3 if direction == 1 else 1  # Zmiana kierunku
                if ny < 0 or ny >= GRID_HEIGHT:
                    ny = y
                    direction = 2 if direction == 0 else 0  # Zmiana kierunku

                # Odbicie od bariery
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and barrier[ny][nx]:
                    nx, ny = x, y  # Pozostań w tej samej komórce
                    direction = {0: 2, 1: 3, 2: 0, 3: 1}[direction]  # Odbicie kierunku

                new_grid[ny][nx].append(direction)
    return new_grid

# Operacja kolizji
def collision(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if 0 in grid[y][x] and 2 in grid[y][x]:  #góra i dół
                grid[y][x].remove(0)
                grid[y][x].remove(2)
                grid[y][x].extend([1, 3])  #  prawo i lewo
            elif 1 in grid[y][x] and 3 in grid[y][x]:  # prawo i lewo
                grid[y][x].remove(1)
                grid[y][x].remove(3)
                grid[y][x].extend([0, 2])  #  góra i dół


# Główna pętla symulacji
def main():
    grid, barrier = initialize_grid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                remove_barrier(barrier, pygame.mouse.get_pos())

        grid = streaming(grid, barrier)
        collision(grid)

        draw_particles_and_barrier(grid, barrier)
        pygame.display.flip()
        clock.tick(20)

    pygame.quit()

if __name__ == "__main__":
    main()
