import math
import pylab
from numpy import float64
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from Form import Ui_MainWindow
from tab_widg import Ui_MainWindow_tab
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
from main import second_window

class mathpart(Ui_MainWindow):
    def building(self, p, v, y, k, c, u10, u20, eps, d, x0, h, secwin):
        count_div, count_mul = 0, 0
        s1_max, s2_max = 0, 0
        h_max, h_min = 0, h
        h_list = []
        def du1(u1, u2):
            return p + k * (u1**2 /u2) - y * u1

        def du2(u1, u2):
            return c * (u1**2) - v * u2
        
        def calc_coef_for_system(du1, du2, u1, u2, step):
            q = [[0] * 2] * 5
            res = np.array(q, dtype = np.float64)
            res[0][0] = du1(u1, u2)
            res[0][1] = du2(u1, u2)
            
            res[1][0] = du1(u1 + step * res[0][0] / 3, u2 + step * res[0][0] / 3)
            res[1][1] = du2(u1 + step * res[0][1] / 3, u2 + step * res[0][1] / 3)
            
            res[2][0] = du1(u1 + step * (res[0][0] + res[1][0]) / 6, u2 + step * (res[0][0] + res[1][0]) / 6)
            res[2][1] = du2(u1 + step * (res[0][1] + res[1][1]) / 6, u2 + step * (res[0][1] + res[1][1]) / 6)

            res[3][0] = du1(u1 + step * (res[0][0] + 3 * res[2][0]) / 8, u2 + step * (res[0][0] + 3 * res[2][0]) / 8)
            res[3][1] = du2(u1 + step * (res[0][1] + 3 * res[2][1]) / 8, u2 + step * (res[0][1] + 3 * res[2][1]) / 8)

            res[4][0] = du1(u1 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2, u2 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2)
            res[4][1] = du2(u1 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2, u2 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2)

            return res
        
        def next_point(x, u1, u2, number_r):
            nonlocal h
            secwin.tableWidget.setRowCount(number_r+1)
            x_new = x + h
            nonlocal h_list
            h_list.append(h)
            K = calc_coef_for_system(du1, du2, u1, u2, h)

            s1 = h * (2 * K[0][0] - 9 * K[2][0] + 8 * K[3][0] - K[4][0]) / 30
            s2 = h * (2 * K[0][1] - 9 * K[2][1] + 8 * K[3][1] - K[4][1]) / 30

            u1_new = u1 + h * (K[0][0] + 4 * K[3][0] + K[4][0]) / 6
            u2_new = u2 + h * (K[0][1] + 4 * K[3][1] + K[4][1]) / 6
            secwin.tableWidget.setItem(number_r, 0, QtWidgets.QTableWidgetItem(str(number_r)))
            secwin.tableWidget.setItem(number_r, 1, QtWidgets.QTableWidgetItem(str(x_new)))
            secwin.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(u1_new)))
            secwin.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(u2_new)))
            nonlocal count_div, count_mul
            if self.checkBox.isChecked():
                nonlocal s1_max, s2_max
                if abs(s1) >= eps/16 and abs(s2) >= eps/16 and abs(s1) <= eps and abs(s2) <= eps:
                    s1_max = max(s1_max, s1)
                    s2_max = max(s2_max, s2)
                    secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(s1)))
                    secwin.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(s2)))
                    secwin.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(h)))
                    return x_new, u1_new, u2_new
                elif abs(s1) > eps or abs(s2) > eps:
                    count_div += 1
                    h /= 2
                    s1_max = max(s1_max, s1)
                    s2_max = max(s2_max, s2)
                    secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(s1)))
                    secwin.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(s2)))
                    secwin.tableWidget.setItem(number_r, 7, QtWidgets.QTableWidgetItem(str(count_div)))
                    return next_point(x, u1, u2, number_r)
                elif abs(s1) < eps/16 and abs(s2) < eps/16:
                    count_mul += 1
                    h *= 2
                    s1_max = max(s1_max, s1)
                    s2_max = max(s2_max, s2)
                    secwin.tableWidget.setItem(number_r, 8, QtWidgets.QTableWidgetItem(str(count_mul)))
                    secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(s1)))
                    secwin.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(s2)))
                    secwin.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(h)))
                    return x_new, u1_new, u2_new
                else: 
                    secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(s1)))
                    secwin.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(s2)))
                    secwin.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(h)))
                    return x_new, u1_new, u2_new
                    
            else: 
                
                secwin.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(h)))
                return x_new, u1_new, u2_new
            

        self.progressBar.setMinimum(x0)
        self.progressBar.setMaximum(d)
        v1, v2 = u10, u20
        x = x0

        secwin.label.setText("Начальное время = " + str(x))
        secwin.label_2.setText("Начальная конц. активатора = " + str(v1))
        secwin.label_3.setText("Начальная конц. ингибитора = " + str(v2))
        secwin.label_4.setText("Плотность активатора k = " + str(p))
        secwin.label_5.setText("Скорость самообразования активатора k = " + str(k))
        secwin.label_6.setText("скорость самообразования ингибитора c = " + str(c))
        secwin.label_7.setText("Естественный распад активатора v = " + str(v))
        secwin.label_8.setText("Естественный распад ингибитора y = " + str(y))
        secwin.label_9.setText("Контроль локальной погрешности Eps = " + str(eps))
        
        x_list, v1_list, v2_list = [x], [v1], [v2]
        i = 0
        while x < d:
            x, v1, v2 = next_point(x, v1, v2, i)
            x_list.append(x)
            v1_list.append(v1)
            v2_list.append(v2)
            self.progressBar.setValue(x)
            i += 1
        plt.subplot(2, 1, 1)
        plt.title('Концентрации')
        plt.ylabel('Активатор')
        if self.checkBox.isChecked():
            plt.plot(x_list, v1_list, 'c', label = 'С контролем ЛП') 
        else:
            plt.plot(x_list, v1_list)
        plt.grid()

        plt.subplot(2, 1, 2)
        plt.ylabel('Ингибитор')
        if self.checkBox.isChecked():
            plt.plot(x_list, v2_list, 'c', label = 'С контролем ЛП')
        else:
            plt.plot(x_list, v2_list)
        if self.checkBox.isChecked():
            secwin.label_10.setText("Максимальная оценка ЛП 1 = " + str(s1_max))
            secwin.label_11.setText("Максимальная оценка ЛП 2 = " + str(s2_max))
            secwin.label_14.setText("Делений шага = " + str(count_div))
            secwin.label_15.setText("Удвоений шага = " + str(count_mul))
        secwin.label_12.setText("Максимальный шаг = " + str(max(h_list)))
        secwin.label_13.setText("Минимальный шаг = " + str(min(h_list)))

        plt.legend()
        plt.grid()
        secwin.show()
        plt.show()