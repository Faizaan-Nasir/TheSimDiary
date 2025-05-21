from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Clock(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
        self.setWindowTitle('Clock')

        # Rectangular hour hand (width: 7, length: 50)
        self.hPointer = QPolygon([
            QPoint(-3, 0),
            QPoint(-3, -50),
            QPoint(3, -50),
            QPoint(3, 0)
        ])
        # Rectangular minute hand (width: 5, length: 70)
        self.mPointer = QPolygon([
            QPoint(-2, 0),
            QPoint(-2, -70),
            QPoint(2, -70),
            QPoint(2, 0)
        ])
        # Rectangular second hand (width: 2, length: 90)
        self.sPointer = QPolygon([
            QPoint(-1, 0),
            QPoint(-1, -90),
            QPoint(1, -90),
            QPoint(1, 0)
        ])

        self.bColor = Qt.black
        self.sColor = Qt.red

    def paintEvent(self, event):
        rec = min(self.width(), self.height())
        from datetime import datetime
        now_utc = datetime.utcnow()
        tik = QTime(now_utc.hour, now_utc.minute, now_utc.second)
        painter = QPainter(self)

        def drawPointer(color, rotation, pointer):
            painter.setBrush(QBrush(color))
            painter.save()
            painter.rotate(rotation)
            painter.drawConvexPolygon(pointer)
            painter.restore()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(rec / 200, rec / 200)
        painter.setPen(QtCore.Qt.NoPen)

        drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * tik.second()), self.sPointer)

        # Draw clock face dashes
        for i in range(0, 60):
            if (i % 5) == 0:
                # Thicker pen for hour marks (number indicators)
                hour_pen = QPen(self.bColor)
                hour_pen.setWidth(5)
                painter.setPen(hour_pen)
                painter.drawLine(82, 0, 97, 0)
            else:
                # Thinner pen for minute marks
                minute_pen = QPen(self.bColor)
                minute_pen.setWidth(2)
                painter.setPen(minute_pen)
                painter.drawLine(92, 0, 97, 0)
            painter.rotate(6)

        painter.end()
