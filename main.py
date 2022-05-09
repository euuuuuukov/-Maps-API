import requests
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QSlider, QPlainTextEdit, QCheckBox


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
        self.set_pt = False
        self.add_index = False
        self.x, self.y, self.dx, self.dy = 200, 200, 200, 200

        self.input_coordx = QLineEdit(self)
        self.input_coordx.move(210, 0)
        self.input_coordx.resize(150, 30)

        self.txt_coordx1 = QLabel(' Введите долготу:', self)
        self.txt_coordx1.resize(210, 15)
        self.txt_coordx1.setFont(QFont('Italic', 10))

        self.txt_coordx2 = QLabel(' (диапазон изменения - от -175 до 175)', self)
        self.txt_coordx2.resize(210, 15)
        self.txt_coordx2.move(0, 15)
        self.txt_coordx2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_coordy = QLineEdit(self)
        self.input_coordy.move(210, 35)
        self.input_coordy.resize(150, 30)

        self.txt_coordy1 = QLabel(' Введите широту:', self)
        self.txt_coordy1.resize(210, 15)
        self.txt_coordy1.move(0, 35)

        self.txt_coordy2 = QLabel(' (диапазон изменения - от -85 до 85)', self)
        self.txt_coordy2.resize(210, 15)
        self.txt_coordy2.move(0, 50)
        self.txt_coordy2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_scalex = QLineEdit(self)
        self.input_scalex.move(210, 70)
        self.input_scalex.resize(150, 30)

        self.txt_scalex1 = QLabel(' Введите разность долгот области:', self)
        self.txt_scalex1.resize(210, 15)
        self.txt_scalex1.move(0, 70)
        self.txt_scalex1.setFont(QFont('Italic', 10))

        self.txt_scalex2 = QLabel(' (диапазон изменения - от 0.005 до 90)', self)
        self.txt_scalex2.resize(210, 15)
        self.txt_scalex2.move(0, 85)
        self.txt_scalex2.setFont(QFont('Italic', 8, QFont.Cursive))

        self.input_scaley = QLineEdit(self)
        self.input_scaley.move(210, 105)
        self.input_scaley.resize(150, 30)

        self.txt_scaley1 = QLabel(' Введите разность широт области:', self)
        self.txt_scaley1.resize(210, 15)
        self.txt_scaley1.move(0, 105)
        self.txt_scaley1.setFont(QFont('Italic', 10))

        self.txt_scaley2 = QLabel(' (диапазон изменения - от 0.005 до 90)', self)
        self.txt_scaley2.resize(210, 15)
        self.txt_scaley2.move(0, 120)
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
        self.slider.resize(355, 25)
        self.slider.move(5, 185)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(50)
        self.slider.valueChanged.connect(self.change_map_type)

        self.slider_txt = QLabel(' схема\t\t\t       гибрид\t\t          спутник', self)
        self.slider_txt.resize(360, 15)
        self.slider_txt.move(0, 215)

        self.map = QLabel(self)
        self.map.move(370, 0)
        self.map.resize(650, 450)

        self.search_txt = QLabel(' Или просто введите\n адрес и нажмите "Искать"', self)
        self.search_txt.resize(140, 30)
        self.search_txt.move(0, 235)

        self.search_input = QPlainTextEdit(self)
        self.search_input.resize(210, 60)
        self.search_input.move(150, 235)

        self.search_btn = QPushButton('Искать', self)
        self.search_btn.resize(140, 30)
        self.search_btn.move(0, 265)
        self.search_btn.clicked.connect(self.search)

        self.search_txt_error = QLabel(self)
        self.search_txt_error.resize(360, 15)
        self.search_txt_error.move(0, 295)
        self.search_txt_error.setFont(QFont('Italic', 8, QFont.Bold))

        self.reset_btn = QPushButton('Сброс поискового результата', self)
        self.reset_btn.resize(200, 30)
        self.reset_btn.move(90, 310)
        self.reset_btn.clicked.connect(self.reset)

        self.txt_all_address = QLabel(' Полный адрес\n найденного объекта:', self)
        self.txt_all_address.resize(115, 35)
        self.txt_all_address.move(0, 345)

        self.all_address = QPlainTextEdit(self)
        self.all_address.resize(240, 35)
        self.all_address.move(120, 345)
        self.all_address.setReadOnly(True)

        self.index_check = QCheckBox('Добавить почтовый индекс к полному адресу', self)
        self.index_check.resize(360, 30)
        self.index_check.move(0, 380)
        self.index_check.clicked.connect(self.index_switch)

    def index_switch(self):
        if self.index_check.isChecked():
            self.add_index = True
        else:
            self.add_index = False
        if self.all_address.toPlainText() != '':
            self.search()

    def reset(self):
        self.search_txt_error.setText('')
        self.map.setPixmap(QPixmap('no_map.jpg'))
        self.txt_error.setText('')
        self.all_address.setPlainText('')
        self.search_input.setPlainText('')
        self.input_coordx.setText('')
        self.input_coordy.setText('')
        self.input_scalex.setText('')
        self.input_scaley.setText('')
        self.set_pt = False
        self.add_index = False
        self.index_check.setChecked(False)

    def search(self):
        try:
            self.set_pt = True
            r = requests.get(f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
                             f'geocode={self.search_input.toPlainText()}&format=json').json()
            r = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            x, y = map(str, r['Point']['pos'].split())
            r = r['metaDataProperty']['GeocoderMetaData']
            if self.add_index:
                self.all_address.setPlainText(f'{r["Address"]["postal_code"]}, {r["text"]}')
            else:
                self.all_address.setPlainText(r["text"])
            self.input_coordx.setText(x)
            self.input_coordy.setText(y)
            self.input_scalex.setText('0.1')
            self.input_scaley.setText('0.1')
            self.txt_error.setText('')
            self.x, self.y = x, y
            self.show_map()
            self.search_txt_error.setText('')
        except:
            self.search_txt_error.setText('Проверьте правильность введенных данных!')

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
        painter.drawLine(0, 232, 369, 232)
        for i in range(0, 369, 3):
            painter.drawLine(i, 342, i + 1, 342)
        painter.end()

    def show_map(self):
        if self.base_bool():
            self.search_txt_error.setText('')
            self.txt_error.setText('')
            if not (self.x == self.input_coordx.text() and self.y == self.input_coordy.text()):
                self.set_pt = False
            self.x, self.y, self.dx, self.dy = self.input_coordx.text(), self.input_coordy.text(), \
                                               self.input_scalex.text(), self.input_scaley.text()
            if self.set_pt:
                self.response = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn='
                                             f'{self.dx},{self.dy}&size=650,450&l={self.map_type}&pt={self.x},{self.y}')
            else:
                self.response = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}'
                                             f'&spn={self.dx},{self.dy}&size=650,450&l={self.map_type}')
            with open('map.png', 'wb') as f:
                f.write(self.response.content)
            self.map.setPixmap(QPixmap('map.png'))
            os.remove('map.png')

    def base_bool(self):
        x, y, dx, dy = self.input_coordx.text(), self.input_coordy.text(), self.input_scalex.text(), \
                       self.input_scaley.text()
        if x == '' or y == '' or dx == '' or dy == '':
            self.txt_error.setText('Заполните все поля!')
            return False
        elif not is__float_number(x) or not is__float_number(y) or not is__float_number(dx) or not is__float_number(dy):
            self.txt_error.setText('Значения должны быть числами!')
            return False
        elif not (float(x) >= -175 and float(x) <= 175) or not (float(y) >= -85 and float(y) <= 85) or \
                not (float(dx) >= 0.005 and float(dx) <= 90) or not (float(dy) >= 0.005 and float(dy) <= 90):
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