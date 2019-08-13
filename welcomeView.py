from PyQt5 import QtCore
from PyQt5.QtCore import *
import sys

from PyQt5.QtGui import QPainter, QPixmap, QIcon
from PyQt5.QtWidgets import *
import res_rc


class WelcomeWindow(QWidget):
    fade_over = pyqtSignal()


    def __init__(self, parent=None):
        super(WelcomeWindow, self).__init__(parent)
        self.initPix()

        self.setWindowTitle('初始化中...')
        # self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 设置透明度
        self.opa = 0

        self.fade_in_Timer = QTimer()
        self.fade_out_Timer = QTimer()

        self.fade_in_Timer.timeout.connect(self.fade_in)
        self.fade_out_Timer.timeout.connect(self.fade_out)

        self.fade_in_Timer.start(10)

    def initPix(self):
        self.pix = QPixmap(":/trans/pic/logo.png", '0', Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither)
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

    def fade_in(self):
        self.opa += 0.01
        self.setWindowOpacity(self.opa)
        if self.opa >= 1.0:
            self.fade_in_Timer.stop()
            QTimer.singleShot(2000, self.fade_out_start)

    def fade_out_start(self):
        self.fade_out_Timer.start(10)

    def fade_out(self):
        self.opa += -0.01
        self.setWindowOpacity(self.opa)
        if self.opa < 0:
            self.fade_out_Timer.stop()
            self.fade_over.emit()
            self.close()

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix.width(), self.pix.height(), self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = WelcomeWindow()

    win.show()

    sys.exit(app.exec_())
