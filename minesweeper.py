import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

class mainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Start!")
        self.grid = {}
        self.text = QtWidgets.QLabel("Welcome to 10x10 Minesweeper!")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setVerticalSpacing(0)

        self.button.clicked.connect(self.startGame)


    def startGame(self):
        self.layout.removeWidget(self.button)
        self.layout.removeWidget(self.text)
        for i in range(10):
            for j in range(10):
                self.grid[(i, j)] = QtWidgets.QPushButton("%d %d" % (i, j))
                self.grid[(i, j)].setFixedSize(50,50)
                self.grid[(i, j)].clicked.connect(self.checkMine)
                self.layout.addWidget(self.grid[(i, j)], i, j)



    def checkMine(self):
        print("checking for mine")



class mineBoard():
    def __init__(self):
        self.numberMines = 10
        self.board = []


    def createBoard(self):
        #initialise the game board
        for i in range(10):
            for j in range(10):
                self.board.append('%d%d' % (i, j)) 
        #add mines to the game board
        for r in range(10):
            newMine = random.randint(0, 99)
            self.board[newMine] = 'M'



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = mainWindow()
    widget.resize(500,500)
    widget.show()

    board = mineBoard()
    board.createBoard()

    sys.exit(app.exec_())