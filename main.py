import requests
import os
import sys
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QDesktopWidget


def is__float_number(n):
    for i in n:
        if i not in '0123456789.':
            return False
    return True


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(1020, 450)
        self.setWindowTitle('Большая задача по Maps API')

        self.input_coordx = QLineEdit(self)
        self.input_coordx.move(210, 0)
        self.input_coordx.resize(150, 30)

        self.txt_coordx1 = QLabel(' Введите долготу:', self)
        self.txt_coordx1.resize(210, 15)
        self.txt_coordx1.setFont(QFont('Italic', 10))

        self.txt_coordx2 = QLabel('\n (диапазон изменения - от -180 до 180)', self)
        self.txt_coordx2.resize(210, 30)
        self.txt_coordx2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_coordy = QLineEdit(self)
        self.input_coordy.move(210, 35)
        self.input_coordy.resize(150, 30)

        self.txt_coordy1 = QLabel(' Введите широту:', self)
        self.txt_coordy1.resize(210, 15)
        self.txt_coordy1.move(0, 35)
        self.txt_coordy1.setFont(QFont('Italic', 10))

        self.txt_coordy2 = QLabel('\n (диапазон изменения - от -90 до 90)', self)
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

        self.txt_scalex2 = QLabel('\n (диапазон изменения - от 1 до 90)', self)
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

        self.txt_scaley2 = QLabel('\n (диапазон изменения - от 1 до 90)', self)
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

        self.map = QLabel(self)
        self.map.move(370, 0)
        self.map.resize(650, 450)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawLine(370, 0, 370, 450)
        painter.end()

    def show_map(self):
        if self.input_coordx.text() == '' or self.input_coordy.text() == '' or self.input_scalex.text() == '' or\
                self.input_scaley.text() == '':
            self.txt_error.setText('Заполните все поля!')
        elif not is__float_number(self.input_coordx.text()) or not is__float_number(self.input_coordy.text()) or\
                not is__float_number(self.input_scalex.text()) or not is__float_number(self.input_scaley.text()):
            self.txt_error.setText('Значения должны быть числами!')
        elif not (float(self.input_coordx.text()) >= -180 and float(self.input_coordx.text()) <= 180) or\
                not (float(self.input_coordy.text()) >= -90 and float(self.input_coordy.text()) <= 90) or\
                not (float(self.input_scalex.text()) >= 1 and float(self.input_scalex.text()) <= 90) or\
                not (float(self.input_coordy.text()) >= 1 and float(self.input_coordy.text()) <= 90):
            self.txt_error.setText('Не все значения находятся\nв указанном диапазоне!')
        else:
            self.txt_error.setText('')
            self.from_request(self.input_coordx.text(), self.input_coordy.text(), self.input_scalex.text(),
                              self.input_scaley.text())


    def from_request(self, x, y, dx, dy):
        self.response = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={dx},{dy}&size=650,450&l=map')
        with open('map.png', 'wb') as f:
            f.write(self.response.content)
        self.pixmap = QPixmap('map.png')
        self.map.setPixmap(self.pixmap)
        os.remove('map.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())