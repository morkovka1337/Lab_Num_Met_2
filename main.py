# -*- coding: utf-8 -*-
import sys
import math
# Импортируем наш интерфейс из файла
from Form import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from MyMplCanc import MtMplCanv
import math_part
from numpy import float64
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtGui, QtCore
from MyMplCanc import MtMplCanv
from MyMplCanc import MtMplCanv2
from matplotlib.figure import Figure
from tab_widg import *
class MyWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.sec_win = None
        self.figure = Figure()
        self.figure2 = Figure()

        # добавление шаблона размещения на виджет
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget)

        self.companovka_for_mpl2 = QtWidgets.QVBoxLayout(self.widget_2)

        # получение объекта класса холста с нашим рисунком

        self.canvas = MtMplCanv(self.figure)

        self.canvas2 = MtMplCanv2(self.figure2)
        # Размещение экземпляра класса холста в шаблоне размещения
        self.companovka_for_mpl.addWidget(self.canvas)

        self.companovka_for_mpl2.addWidget(self.canvas2)
        # получение объекта класса панели управления холста
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        # Размещение экземпляра класса панели управления в шаблоне размещения
        self.companovka_for_mpl.addWidget(self.toolbar)

        self.companovka_for_mpl2.addWidget(self.toolbar2)
        # Здесь прописываем событие нажатия на кнопку
        self.pushButton.clicked.connect(self.MyFunction)

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def MyFunction(self):
        p = float64(self.textEdit.toPlainText())
        v = float64(self.textEdit_2.toPlainText())
        y = float64(self.textEdit_3.toPlainText())
        k = float64(self.textEdit_4.toPlainText())
        c = float64(self.textEdit_5.toPlainText())

        u10 = float64(self.textEdit_6.toPlainText())
        u20 = float64(self.textEdit_7.toPlainText())
        x0 = float64(self.textEdit_10.toPlainText())

        eps = float64(self.textEdit_8.toPlainText())
        d = float64(self.textEdit_9.toPlainText())
        h = float64(self.textEdit_11.toPlainText())
        
        self.sec_win = second_window(self)
        math_part.mathpart.building(self, p, v, y, k, c, u10, u20, eps, d, x0, h, self.sec_win)

class second_window(QMainWindow, Ui_MainWindow_tab):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass