import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class mainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.board_size = 10
        self.num_mines = 10
        self.status = "Playing"

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clock.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%02d" % self.num_mines)
        self.clock.setText("000")

        self.button = QPushButton("Reset")
        self.button.setFixedSize(QSize(70, 50))

        self.button.pressed.connect(self.button_reset)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

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





if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()

    sys.exit(app.exec_())