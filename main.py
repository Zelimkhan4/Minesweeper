import pygame
import sys
import random

pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)

class Board:
    def __init__(self, size):
        self.size = size
        self.mines = []
        self.num_of_mines = 8
        self.board = [[[] for i in range(WIDTH // self.size)] for j in range(HEIGHT // self.size)]
        self.font = pygame.font.SysFont('Arial', 20)    

    def draw_board(self, screen):
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if not col:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(j * self.size, i * self.size, self.size - 5, self.size - 5))
                elif col > 0:
                    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(j * self.size, i * self.size, self.size - 5, self.size - 5))
                    text = self.font.render(str(col), False, (255, 0, 0))
                    screen.blit(text, (j * self.size + text.get_width() // 2, i * self.size + text.get_height() // 2))


    def find_position(self, pos):
        # Позиция мышки
        x, y = pos

        # Позиция относительно моей сетки
        pos_x = x // self.size
        pos_y = y // self.size

        return pos_x, pos_y
    

    def place_mines(self, pos): # Позиция на которую уже нажали(в первый раз)
        x_pos = random.sample(range(WIDTH // self.size), k=self.num_of_mines)
        y_pos = random.sample(range(HEIGHT // self.size), k=self.num_of_mines)
        self.mines = [(i, j) for i, j in zip(x_pos, y_pos) if (i, j) != pos]


    # Открытие ячейки
    def open_cell(self, pos):
        # Рекурсивный алгоритм для открытия клеток
        # Всего три случая 
        # 1. Под клеткой бомба, вы проигрываете
        # 2. Под клеткой нет бомбы но рядом есть, записывается количество бомб рядом с клетки
        # 3. Под клеткой бомбы нет, и рядом нет, для каждого соседа проверяется верхнее
        
        # Мина, game_over
        if pos in self.mines:
            sys.exit()
        x, y = pos
        # Алгоритм для определения соседей
        neighbours = []
        for row in range(y - 1, y + 2):
            if row < 0:
                continue
            for col in range(x - 1, x + 2):
                if col < 0:
                    continue
                elif (col, row) == pos:
                    continue 
                neighbours.append((col, row))

        count_of_bombs = [i in self.mines for i in neighbours].count(True)
        if count_of_bombs:
            # В матрице сначала строка, затем столбцы
            self.board[y][x] = count_of_bombs
            print(x, y)
        else:
            self.board[y][x] = -1
            # for n in neighbours:
            #     try:
            #         self.open_cell(n)
            #     except:
            #         pass

if __name__ == "__main__":
    running = True
    board = Board(40)
    board.open_cell((0, 0))
    start_game = False
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    if not start_game:
                        board.place_mines(ev.pos)
                        start_game = True
                    x, y = ev.pos
                    board.open_cell((x // board.size, y // board.size))
        screen.fill((0, 0, 0))
        board.draw_board(screen)

        # Some actions

        pygame.display.flip()