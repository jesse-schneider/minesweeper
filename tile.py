from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

FLAG_IMAGE = QImage("./image/flag-cross.png")
MINE_IMAGE = QImage("./image/mine.png")

class Tile(QWidget):
    expand = pyqtSignal(int, int)
    clicked = pyqtSignal()
    clicked_mine = pyqtSignal()
    size = 300
    xAx = (3**0.5 / 2)
    hexaPoints = [QPoint(size/4,0),
                    QPoint(size/4 + size/2,0),
                    QPoint(size,size*0.5*xAx),
                    QPoint(size/4 + size/2,size*xAx),
                    QPoint(size/4,size*xAx),
                    QPoint(0,size*0.5*xAx)]

    hexaPointsF = [QPointF(size/4,0),
                    QPointF(size/4 + size/2,0),
                    QPointF(size,size*0.5*xAx),
                    QPointF(size/4 + size/2,size*xAx),
                    QPointF(size/4,size*xAx),
                    QPointF(0,size*0.5*xAx)]
    hexa = QPolygon(hexaPoints)
    hexaF = QPolygonF(hexaPoints)

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
        p.drawPolygon(*Tile.hexaF)

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