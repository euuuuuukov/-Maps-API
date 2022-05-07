import requests
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QSlider


def is__float_number(n):
    if not n[0] in '-0123456789':
        return False
    for i in n[1:]:
        if i not in '-0123456789.':
            return False
    return True


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(1020, 450)
        self.setWindowTitle('Большая задача по Maps API')
        self.map_type = 'map'

        self.input_coordx = QLineEdit(self)
        self.input_coordx.move(210, 0)
        self.input_coordx.resize(150, 30)

        self.txt_coordx1 = QLabel(' Введите долготу:', self)
        self.txt_coordx1.resize(210, 15)
        self.txt_coordx1.setFont(QFont('Italic', 10))

        self.txt_coordx2 = QLabel('\n (диапазон изменения - от -175 до 175)', self)
        self.txt_coordx2.resize(210, 30)
        self.txt_coordx2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_coordy = QLineEdit(self)
        self.input_coordy.move(210, 35)
        self.input_coordy.resize(150, 30)

        self.txt_coordy1 = QLabel(' Введите широту:', self)
        self.txt_coordy1.resize(210, 15)
        self.txt_coordy1.move(0, 35)
        self.txt_coordy1.setFont(QFont('Italic', 10))

        self.txt_coordy2 = QLabel('\n (диапазон изменения - от -85 до 85)', self)
        self.txt_coordy2.resize(210, 30)
        self.txt_coordy2.move(0, 35)
        self.txt_coordy2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_scalex = QLineEdit(self)
        self.input_scalex.move(210, 70)
        self.input_scalex.resize(150, 30)

        self.txt_scalex1 = QLabel(' Введите разность долгот области:', self)
        self.txt_scalex1.resize(210, 15)
        self.txt_scalex1.move(0, 70)
        self.txt_scalex1.setFont(QFont('Italic', 10))

        self.txt_scalex2 = QLabel('\n (диапазон изменения - от 0.005 до 90)', self)
        self.txt_scalex2.resize(210, 30)
        self.txt_scalex2.move(0, 70)
        self.txt_scalex2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_scaley = QLineEdit(self)
        self.input_scaley.move(210, 105)
        self.input_scaley.resize(150, 30)

        self.txt_scaley1 = QLabel(' Введите разность широт области:', self)
        self.txt_scaley1.resize(210, 15)
        self.txt_scaley1.move(0, 105)
        self.txt_scaley1.setFont(QFont('Italic', 10))

        self.txt_scaley2 = QLabel('\n (диапазон изменения - от 0.005 до 90)', self)
        self.txt_scaley2.resize(210, 30)
        self.txt_scaley2.move(0, 105)
        self.txt_scaley2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.txt_point = QLabel('  Разделитель - точка!', self)
        self.txt_point.move(0, 135)
        self.txt_point.resize(150, 10)
        self.txt_point.setFont(QFont('Italic', 8, QFont.Cursive))

        self.btn_showmap = QPushButton('Показать карту!', self)
        self.btn_showmap.resize(100, 30)
        self.btn_showmap.move(0, 150)
        self.btn_showmap.clicked.connect(self.show_map)

        self.txt_error = QLabel(self)
        self.txt_error.resize(250, 30)
        self.txt_error.move(110, 150)
        self.txt_error.setFont(QFont('Italic', 8, QFont.Bold))

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.resize(360, 25)
        self.slider.move(0, 185)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(50)
        self.slider.valueChanged.connect(self.change_map_type)

        self.slider_txt = QLabel('схема\t\t\t       гибрид\t\t          спутник', self)
        self.slider_txt.resize(360, 15)
        self.slider_txt.move(0, 215)

        self.map = QLabel(self)
        self.map.move(370, 0)
        self.map.resize(650, 450)

    def change_map_type(self, value):
        if value < 34:
            self.map_type = 'map'
            self.slider.setValue(0)
        elif value > 66:
            self.map_type = 'sat'
            self.slider.setValue(100)
        else:
            self.map_type = 'sat,skl'
            self.slider.setValue(50)
        if self.base_bool():
            self.show_map()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawLine(369, 0, 369, 450)
        painter.drawLine(0, 182, 369, 182)
        painter.end()

    def show_map(self):
        if self.base_bool():
            self.txt_error.setText('')
            self.from_request(self.input_coordx.text(), self.input_coordy.text(), self.input_scalex.text(),
                              self.input_scaley.text())

    def from_request(self, x, y, dx, dy):
        self.response = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={dx},{dy}&size=650,450&'
                                     f'l={self.map_type}')
        with open('map.png', 'wb') as f:
            f.write(self.response.content)
        self.pixmap = QPixmap('map.png')
        self.map.setPixmap(self.pixmap)
        os.remove('map.png')

    def base_bool(self):
        if self.input_coordx.text() == '' or self.input_coordy.text() == '' or self.input_scalex.text() == '' or\
                self.input_scaley.text() == '':
            self.txt_error.setText('Заполните все поля!')
            return False
        elif not is__float_number(self.input_coordx.text()) or not is__float_number(self.input_coordy.text()) or\
                not is__float_number(self.input_scalex.text()) or not is__float_number(self.input_scaley.text()):
            self.txt_error.setText('Значения должны быть числами!')
            return False
        elif not (float(self.input_coordx.text()) >= -175 and float(self.input_coordx.text()) <= 175) or\
                not (float(self.input_coordy.text()) >= -85 and float(self.input_coordy.text()) <= 85) or\
                not (float(self.input_scalex.text()) >= 0.005 and float(self.input_scalex.text()) <= 90) or\
                not (float(self.input_scaley.text()) >= 0.005 and float(self.input_scaley.text()) <= 90):
            self.txt_error.setText('Не все значения находятся\nв указанном диапазоне!')
            return False
        return True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.base_bool():
                if float(self.input_scalex.text()) <= 0.015:
                    self.input_scalex.setText('0.005')
                else:
                    self.input_scalex.setText(str(float(self.input_scalex.text()) - 0.01))
                if float(self.input_scaley.text()) <= 0.015:
                    self.input_scaley.setText('0.005')
                else:
                    self.input_scaley.setText(str(float(self.input_scaley.text()) - 0.01))
                self.txt_error.setText('')
                self.show_map()
        elif event.key() == Qt.Key_PageDown:
            if self.base_bool():
                if float(self.input_scalex.text()) >= 89.99:
                    self.input_scalex.setText('90.000')
                else:
                    self.input_scalex.setText(str(float(self.input_scalex.text()) + 0.01))
                if float(self.input_scaley.text()) >= 89.99:
                    self.input_scaley.setText('90.000')
                else:
                    self.input_scaley.setText(str(float(self.input_scaley.text()) + 0.01))
                self.txt_error.setText('')
                self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
