import unittest
import pygame as pg
from board import *

pg.init()

class TestOpenCell(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main(verbosity=2)
