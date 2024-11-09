import pygame
import sys
import time 
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Настройки окна
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10  # Начальный размер клетки
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
GREEN = (23, 233, 86)

DRAW_WIDTH = WIDTH + 200
# Ширина боковой панели
SIDE_PANEL_WIDTH = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rasterization Algorithms")

# Функции для отрисовки сетки и координат
def draw_grid():
    for x in range(SIDE_PANEL_WIDTH, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (WIDTH, y))
    
    pygame.draw.line(screen,GREEN, (DRAW_WIDTH/2, HEIGHT), (DRAW_WIDTH/2, 0))
    pygame.draw.line(screen,GREEN, (SIDE_PANEL_WIDTH, HEIGHT/2), (WIDTH, HEIGHT/2))

    risk = 600 / GRID_SIZE

    font = pygame.font.SysFont('Arial', 8)

    for i in range(int(risk)):
        text_pos = font.render(f'{i}', True, GREEN)
        text_neg = font.render(f'{-i}', True, GREEN)
        screen.blit(text_pos, (200 + 300 + i * GRID_SIZE, HEIGHT/2))
        screen.blit(text_neg, (200 + 300 - i * GRID_SIZE, HEIGHT/2))
        screen.blit(text_pos, (200 + 300, HEIGHT/2 - i * GRID_SIZE))
        screen.blit(text_neg, (200 + 300, HEIGHT/2 + i * GRID_SIZE))


def draw_pixel(x, y, color=RED):
    if x * GRID_SIZE >= SIDE_PANEL_WIDTH:
        pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def step_by_step(x0, y0, x1, y1):
    start_time = time.time()

    if x0 == x1:
        return [(x0, y) for y in range(min(y0, y1), max(y0, y1) + 1)]
    points = []
    dx = x1 - x0
    dy = y1 - y0
    k = dy / dx
    b = y0 - k * x0
    step = 1 / max(abs(dx), abs(dy))
    x = x0
    if dx > 0:
        while x <= x1:
            y = k * x + b
            points.append((round(x), round(y)))
            x += step
    else:
        while x >= x1:
            y = k * x + b
            points.append((round(x), round(y)))
            x -= step
    print(f'time execution of step by step - {1000000 * (time.time() - start_time)}* 10-6')

    return points

def dda_algorithm(x0, y0, x1, y1):
    start_time = time.time()

    dx, dy = x1 - x0, y1 - y0
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    points = []
    x, y = x0, y0
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    print(f'time execution of dda - {1000000 * (time.time() - start_time)}* 10-6')

    return points

def bresenham_line(x0, y0, x1, y1):
    start_time = time.time()

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    points = []
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    print(f'time execution of bresenham for line - {1000000 * (time.time() - start_time)}* 10-6')

    return points

def bresenham_circle(xc, yc, r):
    start_time = time.time()
    points = []
    x = r
    y = 0
    d = 1 - r
    while x >= y:
        for xi, yi in [(x, y), (y, x), (-x, y), (-y, x), (x, -y), (-x, -y), (y, -x), (-y, -x)]:
            points.append((xc + xi, yc + yi))
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * y - 2 * x + 1

    print(f'time execution of bresenham for circle - {1000000 * (time.time() - start_time)}* 10-6')



    return points

# Основной класс для управления приложением
class RasterizationApp:
    def __init__(self):
        self.algorithm = "Bresenham"
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.drawing = False
        self.radius = 0
        self.input_radius = ""
        self.drawn_points = []
        self.grid_size = GRID_SIZE  # Сохранение начального размера клетки

    def draw_algorithm(self):
        x0, y0 = self.start_point
        if self.algorithm == "Circle":
            r = self.radius
            points = bresenham_circle(x0, y0, r)
        else:
            x1, y1 = self.end_point
            if self.algorithm == "Step by Step":
                points = step_by_step(x0, y0, x1, y1)
            elif self.algorithm == "DDA":
                points = dda_algorithm(x0, y0, x1, y1)
            elif self.algorithm == "Bresenham":
                points = bresenham_line(x0, y0, x1, y1)
        self.drawn_points.extend(points)

    def draw_sidebar(self):
        pygame.draw.rect(screen, GRAY, (0, 0, SIDE_PANEL_WIDTH, HEIGHT))
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(f'Алгоритм:', True, WHITE)
        text2 = font.render(f'{self.algorithm}', True, WHITE)
        screen.blit(text, (10, 10))
        screen.blit(text2, (10,30))

        radius_text = font.render(f'Радиус: {self.input_radius}', True, WHITE)
        screen.blit(radius_text, (10, 50))

        grid_size_text = font.render(f'Размер клетки: {self.grid_size}', True, WHITE)
        screen.blit(grid_size_text, (10, 80))

        # Кнопки для изменения масштаба
        increase_button = font.render('Увеличить масштаб', True, WHITE)
        screen.blit(increase_button, (10, 120))

        decrease_button = font.render('Уменьшить масштаб', True, WHITE)
        screen.blit(decrease_button, (10, 150))

        algorithms = ["Step by Step", "DDA", "Bresenham", "Circle", "Clear"]
        for i, algo in enumerate(algorithms):
            button_color = LIGHT_GRAY if self.algorithm == algo else WHITE
            label = font.render(algo, True, button_color)
            screen.blit(label, (10, 200 + i * 30))

    def redraw_all(self):
        for x, y in self.drawn_points:
            draw_pixel(x, y)

    def run(self):
        global GRID_SIZE
        clock = pygame.time.Clock()
        while True:
            screen.fill(BLACK)
            draw_grid()
            self.draw_sidebar()
            self.redraw_all()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] >= SIDE_PANEL_WIDTH:
                            if self.algorithm == "Circle":
                                self.start_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                if self.input_radius.isdigit():
                                    self.radius = int(self.input_radius)
                                    self.draw_algorithm()
                            else:
                                if not self.drawing:
                                    self.start_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                    self.drawing = True
                                else:
                                    self.end_point = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                                    self.draw_algorithm()
                                    self.drawing = False
                        else:
                            # Проверка нажатия на кнопки изменения масштаба
                            if 120 <= event.pos[1] <= 140:
                                # Увеличить масштаб
                                self.grid_size = min(50, self.grid_size + 1)
                                GRID_SIZE = self.grid_size
                                self.drawn_points.clear()
                            elif 150 <= event.pos[1] <= 170:
                                # Уменьшить масштаб
                                self.grid_size = max(1, self.grid_size - 1)
                                GRID_SIZE = self.grid_size
                                self.drawn_points.clear()
                            
                            # Проверка нажатия на кнопки выбора алгоритмов
                            for i, algo in enumerate(["Step by Step", "DDA", "Bresenham", "Circle", "Clear"]):
                                if 200 + i * 30 <= event.pos[1] <= 200 + i * 30 + 20:
                                    if algo == "Clear":
                                        self.drawn_points.clear()
                                    else:
                                        self.algorithm = algo
                                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_radius.isdigit():
                            self.radius = int(self.input_radius)
                        self.input_radius = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_radius = self.input_radius[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.input_radius += event.unicode

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    app = RasterizationApp()
    app.run()
