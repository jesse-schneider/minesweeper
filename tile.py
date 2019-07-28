from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tile import Tile as Tile

class Tile(QWidget):
    expand = pyqtSignal(int, int)
    clicked = pyqtSignal()
    clicked_mine = pyqtSignal()

    def __init__(self, x, y):
        super(Tile, self).__init__()
        self.setFixedSize(QSize(50, 50))
        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.mine = False
        self.adjacent_n = 0
        self.revealed = False
        self.flagged = False
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rectangle = event.rect()
        if self.revealed:
            colour = self.palette().color(QPalette.Background)
            outer, inner = colour, colour
        else:
            outer, inner = Qt.red, Qt.darkGray

        p.fillRect(rectangle, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(rectangle)

        if self.revealed:
            if self.mine:
                p.drawPixmap(rectangle, QPixmap(MINE_IMAGE))
            elif self.adjacent_n > 0:
                pen = QPen(QColor('#000000'))
                p.setPen(pen)
                f = p.font()
                p.setFont(f)
                p.drawText(rectangle, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))
        elif self.flagged:
            p.drawPixmap(rectangle, QPixmap(FLAG_IMAGE))

    def flag(self):
        self.flagged = not self.flagged
        self.update()
        self.clicked.emit()

    def reveal(self):
        self.revealed = True
        self.update()

    def click(self):
        if not self.revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expand.emit(self.x, self.y)
        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        if (e.button() == Qt.RightButton and not self.revealed):
            self.flag()
        elif (e.button() == Qt.LeftButton):
            self.click()
            if self.mine:
                self.clicked_mine.emit()