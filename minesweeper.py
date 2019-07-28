import sys
import random
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tile import Tile as Tile

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()

        self.board_size = 10
        self.num_mines = 10
        self.status = "Playing"

        window = QWidget()
        horizon_layout = QHBoxLayout()

        self.mines = QLabel()
        self.mines_text = QLabel("Mines: ")
        self.mines.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.mines_text.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock_text = QLabel("Time: ")
        self.clock.setAlignment(Qt.AlignLeft| Qt.AlignVCenter)
        self.clock_text.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        font = self.mines.font()
        font.setPointSize(20)
        font.setWeight(50)
        self.mines.setFont(font)
        self.mines_text.setFont(font)
        self.clock.setFont(font)
        self.clock_text.setFont(font)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%02d" % self.num_mines)
        self.clock.setText("000")

        self.button = QPushButton("Reset")
        self.button.setFixedSize(QSize(70, 50))

        self.button.pressed.connect(self.button_reset)

        horizon_layout.addWidget(self.mines_text)
        horizon_layout.addWidget(self.mines)
        horizon_layout.addWidget(self.clock_text)
        horizon_layout.addWidget(self.clock)
        horizon_layout.addWidget(self.button)

        vert_layout = QVBoxLayout()
        vert_layout.addLayout(horizon_layout)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vert_layout.addLayout(self.grid)
        window.setLayout(vert_layout)
        self.setCentralWidget(window)
      

        self.create_board()

        self.reset_map()
        self.show()

    def create_board(self):
        # Add positions to the board
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                tile = Tile(i, j)
                self.grid.addWidget(tile, i, j)
                # Connect signals to cell for starting game, expanding area and ending game 
                tile.clicked.connect(self.start_game)
                tile.expand.connect(self.expand_reveal_area)
                tile.clicked_mine.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                tile = self.grid.itemAtPosition(y, x).widget()
                tile.reset()
        # Add mines to the positions
        positions = []
        while len(positions) < self.num_mines:
            x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.mine = True
                positions.append((x, y))
        self.status = "playing"

        def get_adjacency_n(x, y):
            positions = self.get_surrounding(x, y)
            num_mines = sum(1 if w.mine else 0 for w in positions)
            return num_mines
        # Add adjacencies to the positions
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_n = get_adjacency_n(x, y)


    def get_surrounding(self, x, y):
        positions = []
        for xi in range(max(0, x - 1), min(x + 2, self.board_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())
        return positions

    def show_mines(self):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()

    def expand_reveal_area(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.board_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.mine:
                    w.click()

    def start_game(self, *args):
        if self.status != "playing":
            self.status = "playing"
            # Start the timer
            self._timer_start_nsecs = int(time.time())
    
    def update_timer(self):
        if self.status == "playing":
            secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % secs)
    
    def button_reset(self):
        if self.status == "playing":
            self.status = "failed"
            self.show_mines()

        elif self.status == "failed":
            self.status = "playing"
            self.reset_map()

    def game_over(self):
        self.show_mines()
        self.status = "failed"


if __name__ == '__main__':
    app = QApplication([])
    window = main_window()
    sys.exit(app.exec_())