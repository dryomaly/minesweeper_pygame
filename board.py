import pygame as pg
import random
from const import WIDTH, HEIGHT


class Cell:
    def __init__(self, x, y,
                 cell_size,
                 radius=3,
                 ):
        self.rect = pg.Rect(x, y, cell_size, cell_size) # ХИТБОКС 
        self.is_mined = False
        self.mines_around = 0
        self.cell_state = 'closed'
        self.radius = radius

    def open(self):
        if self.cell_state == 'closed':
            self.cell_state = 'opened'

    def draw(self, screen):
        if self.cell_state == 'opened':
            cell_color = pg.Color('LemonChiffon')
        elif self.cell_state == 'closed':
            cell_color = pg.Color('ForestGreen')

        visible_rect = self.rect.inflate(-2, -2) # видимая часть хитбокса 
        pg.draw.rect(screen, cell_color, visible_rect, border_radius=self.radius)


class Board:
    def __init__(self, rows, cols, cell_size, mines):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.mines = mines

        # отступы по ширине и высоте
        self.x = (WIDTH - cols * cell_size) // 2 # Ширина экрана - Ширина поля
        self.y = (HEIGHT - rows * cell_size) // 2 # Высота экрана - Высота поля

        self.cells = []
        for row in range(rows):
            line = []
            for col in range(cols):
                cell_x = self.x + col * cell_size
                cell_y = self.y + row * cell_size
                line.append(Cell(cell_x, cell_y, cell_size))
            self.cells.append(line)

        self.placing_mines()

    def placing_mines(self):
        all_cells = []
        for line in self.cells:
            for cell in line:
                all_cells.append(cell)

        mined_cells = random.sample(all_cells, self.mines)
        for cell in mined_cells:
            cell.is_mined = True

    def clicked_cell(self, pos):
        x, y = pos
        col = (x - self.x) // self.cell_size
        row = (y - self.y) // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def draw(self, screen):
        for line in self.cells:
            for cell in line:
                cell.draw(screen)
