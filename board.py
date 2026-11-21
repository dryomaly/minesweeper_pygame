import pygame as pg
import random
from const import *


class Cell:
    def __init__(self, x, y,
                 cell_size,
                 flag_image,
                 row,
                 col,
                 radius=3,
                 ):
        self.rect = pg.Rect(x, y, cell_size, cell_size) # ХИТБОКС 
        self.is_mined = False
        self.mines_around = 0
        self.cell_state = 'closed'
        self.flag_image = flag_image
        self.row = row
        self.col = col
        self.radius = radius
        self.font = pg.font.SysFont('Arial Black', cell_size // 2)

    
    def open(self):
        if self.cell_state == 'closed':
            self.cell_state = 'opened'

    def toggle_flag(self):
        if self.cell_state == 'closed':
            self.cell_state = 'flagged'
        elif self.cell_state == 'flagged':
            self.cell_state = 'closed'
    
    def draw(self, screen):
        rowcol_sum = (self.row + self.col) % 2
        if self.cell_state == "opened" and self.is_mined == True:
            cell_color = COLOR_MINE_CELL
        elif self.cell_state == "opened":
            if self.mines_around == 0:
                cell_color = COLOR_OPENED_CELL_EMPTY
            else:
                cell_color = COLOR_OPENED_CELL_NUMBER
        elif self.cell_state == "closed" or self.cell_state == "flagged":
            if rowcol_sum != 0:
                cell_color = COLOR_CLOSED_CELL_1
            else:
                cell_color = COLOR_CLOSED_CELL_2

        visible_rect = self.rect.inflate(-2, -2) # видимая часть ХИТБОКСА
        pg.draw.rect(screen, cell_color, visible_rect, border_radius=self.radius)
        
        if self.cell_state == 'opened' \
                and self.mines_around > 0 \
                and self.is_mined == False:
            text = self.font.render(str(self.mines_around), True, COLOR_CELL_NUMS[self.mines_around])
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

        if self.cell_state == 'flagged':
            flag_rect = self.flag_image.get_rect(center=visible_rect.center)
            screen.blit(self.flag_image, flag_rect)


class Board:
    def __init__(self, rows, cols, cell_size, mines):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.mines = mines

        # отступы по ширине и высоте
        self.x = (WIDTH - cols * cell_size) // 2 # Ширина экрана - Ширина поля
        self.y = (HEIGHT - rows * cell_size) // 2 # Высота экрана - Высота поля

        self.flag_image = pg.image.load("Images/FLAG.png").convert_alpha()
        self.flag_image = pg.transform.scale(self.flag_image, (cell_size - 8, cell_size - 8))


        self.cells = []
        for row in range(rows):
            line = []
            for col in range(cols):
                cell_x = self.x + col * cell_size
                cell_y = self.y + row * cell_size
                line.append(Cell(cell_x, cell_y, cell_size, self.flag_image, row, col))
            self.cells.append(line)

        self.placing_mines()
        self.count_mines_around()

    def placing_mines(self):
        all_cells = []
        for line in self.cells:
            for cell in line:
                all_cells.append(cell)

        mined_cells = random.sample(all_cells, self.mines)
        for cell in mined_cells:
            cell.is_mined = True

    def count_mines_around(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.is_mined == True:
                    continue

                num_of_mines_around = 0
                for nr in (-1, 0, 1):
                    for nc in (-1, 0, 1):
                        nrow = row + nr
                        ncol = col + nc
                        if 0 <= nrow < self.rows and 0 <= ncol < self.cols:
                            if self.cells[nrow][ncol].is_mined:
                                num_of_mines_around += 1
                cell.mines_around = num_of_mines_around

    def clicked_cell(self, pos):
        x, y = pos
        col = (x - self.x) // self.cell_size
        row = (y - self.y) // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    # Рекурсия / ПРОВЕРИТЬ НА СВЕЖУЮ ГОЛОВУ 
    def open_empty_cells(self, cell):
        if cell.cell_state != "closed":
            return None
        cell.open()

        if cell.mines_around > 0 or cell.is_mined == True:
            return None

        for nr in (-1, 0, 1):
            for nc in (-1, 0, 1):
                nrow = cell.row + nr
                ncol = cell.col + nc
                if 0 <= nrow < self.rows and 0 <= ncol < self.cols:
                    self.open_empty_cells(self.cells[nrow][ncol])
                    

    def draw(self, screen):
        for line in self.cells:
            for cell in line:
                cell.draw(screen)

    def mark_all_mines_on_lost(self):
        for line in self.cells:
            for cell in line:
                if cell.is_mined == True:
                    cell.open()

    def mark_all_mines_on_won(self):
        for line in self.cells:
            for cell in line:
                if cell.is_mined == True:
                    cell.cell_state = "flagged"
