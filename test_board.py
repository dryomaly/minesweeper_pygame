import unittest
import pygame as pg
from board import *

pg.init()

class TestCell(unittest.TestCase):
    def setUp(self):
        self.test_cell = Cell(67, 67, 52, None, 1, 1)

    def test_open_closed_cell(self):
        self.test_cell.open_cell()
        self.assertEqual(self.test_cell.cell_state, "opened")

    def test_open_opened_cell(self):
        self.test_cell.open_cell()
        self.test_cell.open_cell()
        self.assertEqual(self.test_cell.cell_state, "opened")

    def test_open_flagged_cell(self):
        self.test_cell.toggle_flag()
        self.test_cell.open_cell()
        self.assertEqual(self.test_cell.cell_state, "flagged")

    def test_is_flag_set(self):
        self.test_cell.toggle_flag()
        self.assertEqual(self.test_cell.cell_state, "flagged")

    def test_is_flag_removed(self):
        self.test_cell.toggle_flag()
        self.test_cell.toggle_flag()
        self.assertEqual(self.test_cell.cell_state, "closed")


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.screen = pg.display.set_mode((600, 600))
        self.board_10x10 = Board(10, 10, 40, 30)
        self.board_2x3 = Board(2, 3, 10, 2)

    def test_amount_of_mines(self):
        count = 0
        for line in self.board_10x10.cells:
            for cell in line:
                if cell.is_mined:
                    count += 1
        self.assertEqual(count, 30)

    def test_amount_of_mines_around(self):
        mined_cell_1 = self.board_2x3.cells[0][0]
        mined_cell_2 = self.board_2x3.cells[1][0]
        for line in self.board_2x3.cells:
            for cell in line:
                if cell != mined_cell_1 and cell != mined_cell_2:
                    cell.is_mined = False
                else:
                    cell.is_mined = True
        self.board_2x3.count_mines_around()
        self.assertEqual(self.board_2x3.cells[0][1].mines_around, 2)
        self.assertEqual(self.board_2x3.cells[1][1].mines_around, 2)
        self.assertEqual(self.board_2x3.cells[0][2].mines_around, 0)
        self.assertEqual(self.board_2x3.cells[1][2].mines_around, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
