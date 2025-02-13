# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        # self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass


class AnimationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        vbox = QtWidgets.QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        vbox.addWidget(self.canvas)

        hbox = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("start", self)
        self.stop_button = QtWidgets.QPushButton("stop", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.x = np.linspace(0, 5 * np.pi, 400)
        self.p = 0.0
        self.y = np.sin(self.x + self.p)
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=2)

    def update_line(self, i):
        self.p += 0.1
        y = np.sin(self.x + self.p)
        self.line.set_ydata(y)
        return [self.line]

    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line,
                                 blit=True, interval=1)

    def on_stop(self):
        self.ani._stop()


if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())

