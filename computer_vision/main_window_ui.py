"""main_window_ui.py: DATBAC23 Control system Main Window UI code."""
__author__ = "Asbjørn Stokka"
__copyright__ = "Copyright 2021, ELE320"
__credits__ = ["Asbjørn Stokka"]
__license__ = "Apache-2.0"
__version__ = "0.1.0"
__maintainer__ = "Asbjørn Stokka"
__email__ = "asbjorn@maxit-as.com"
__status__ = "Testing"

from defines import *

from PyQt6 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget, plot
from random import randint
import sys
import time

class Ui(QtWidgets.QMainWindow):
    def __init__(self, ui_file, connection: tuple[str, int], fullscreen):
        self.connection_details = connection

        self.app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(ui_file, self) # Load the .ui file


        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        #self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

#        self.update_plot_data()

        if fullscreen:
            self.showFullScreen()
        self.show()
        self.app.exec()

    #def update_plot_data(self):

