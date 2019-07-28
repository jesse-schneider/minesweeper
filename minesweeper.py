import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tile import Tile as Tile

class main_window(QWidget):
    def __init__(self):
        super(main_window, self).__init__()

        self.board_size = 10
        self.num_mines = 10
        self.status = "Playing"

        window = QWidget()
        horizon_layout = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        font = self.mines.font()
        font.setPointSize(24)
        font.setWeight(75)
        self.mines.setFont(font)
        self.clock.setFont(font)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%02d" % self.num_mines)
        self.clock.setText("000")

        self.button = QPushButton("Reset")
        self.button.setFixedSize(QSize(70, 50))

        self.button.pressed.connect(self.button_reset)

        horizon_layout.addWidget(self.mines)
        horizon_layout.addWidget(self.button)
        horizon_layout.addWidget(self.clock)

        vert_layout = QVBoxLayout()
        vert_layout.addLayout(horizon_layout)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vert_layout.addLayout(self.grid)
        window.setLayout(vert_layout)
      

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





if __name__ == '__main__':
    app = QApplication([])
    window = main_window()
    sys.exit(app.exec_())