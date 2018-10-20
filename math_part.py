import math
import pylab
import numpy as np
from numpy import float64
from matplotlib import mlab
from matplotlib.figure import Figure
from Form import Ui_MainWindow
from tab_widg import Ui_MainWindow_tab
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
from main import second_window

class mathpart(Ui_MainWindow):
    def building(self, p, v, y, k, c, u10, u20, eps, d, x0, h):
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
            

        def next_point(x, u1, u2, step):
            nonlocal h

            x_new = x + step

            K = calc_coef_for_system(du1, du2, u1, u2, step)

            s1 = step * (2 * K[0][0] - 9 * K[2][0] + 8 * K[3][0] - K[4][0]) / 30
            s2 = step * (2 * K[0][1] - 9 * K[2][1] + 8 * K[3][1] - K[4][1]) / 30

            u1_new = u1 + step * (K[0][0] + 4 * K[3][0] + K[4][0]) / 6
            u2_new = u2 + step * (K[0][1] + 4 * K[3][1] + K[4][1]) / 6

            if self.checkBox.isChecked():
                if abs(s1) >= eps/16 and abs(s2) >= eps/16 and abs(s1) <= eps and abs(s2) <= eps:
                    return x_new, u1_new, u2_new
                elif abs(s1) > eps or abs(s2) > eps:
                    step /= 2
                    return next_point(x, u1, u2, step)
                elif abs(s1) < eps/16 and abs(s2) < eps/16:
                    step *= 2
                    return x_new, u1_new, u2_new
                else: 
                    return x_new, u1_new, u2_new
                    
            else: 
                return x_new, u1_new, u2_new

        self.progressBar.setMinimum(x0)
        self.progressBar.setMaximum(100)
        ax_1 = self.figure.add_subplot(111)
        ax_2 = self.figure2.add_subplot(111)
        #if self.checkBox2.isChecked():
        #    ax_1.clear()
        #    ax_2.clear()
        ax_1.axis([-5, 10, -5, 20])
        ax_2.axis([-5, 10, -5, 20])
        v1, v2 = u10, u20
        x = x0
        i = 0
        while x < d:
            i += 1
            x_old, v1_old, v2_old = x, v1, v2
            x, v1, v2 = next_point(x, v1, v2, h)
            self.progressBar.setValue(i)
            ax_1.plot([x_old, x], [v1_old, v1], '-r')
            ax_2.plot([x_old, x], [v2_old, v2], '-r')
        ax_1.grid(True)
        ax_2.grid(True)
        self.canvas.draw()
        self.canvas2.draw()
        
        