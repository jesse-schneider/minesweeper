import sys
import random
import time
import unittest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from minesweeper import minesweeper as minesweeper

app = QApplication(sys.argv)

class minesweeper_test(unittest.TestCase):

    form = minesweeper()

    def testingGUI(self):
        self.assertEqual(self.form.board_size, 10)

    def testing_mines(self):
        self.assertEqual(self.form.num_mines, 10)
    
    def testing_grid(self):
        for x in range(0, self.form.board_size):
            for y in range(0, self.form.board_size):
                tile = self.form.grid.itemAtPosition(y, x).widget()
                self.assertEqual(tile.revealed, False)
    
    def testing_flags(self):
        for x in range(0, self.form.board_size):
            for y in range(0, self.form.board_size):
                tile = self.form.grid.itemAtPosition(y, x).widget()
                self.assertEqual(tile.flagged, False)

    def testing_reset(self):
        self.assertEqual(self.form.button.text(), "Reset")

    def testing_clock(self):
        self.assertEqual(self.form.timer_start_secs, int(time.time()))

    def testing_mines_count(self):
        self.assertEqual(self.form.mines.text(), '10')





if __name__ == '__main__':
    test = minesweeper_test()
    unittest.main()