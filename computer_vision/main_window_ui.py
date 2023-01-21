"""main_window_ui.py: DATBAC23 Control system Main Window UI code."""
__author__ = "Asbjørn Stokka"
__copyright__ = "Copyright 2021, ELE320"
__credits__ = ["Asbjørn Stokka"]
__license__ = "Apache-2.0"
__version__ = "0.1.0"
__maintainer__ = "Asbjørn Stokka"
__email__ = "asbjorn@maxit-as.com"
__status__ = "Testing"

import sys
# import time
# from defines import *
from camera_handler.camera_handler import CameraHandler
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QThread, pyqtSignal, QObject
# from pyqtgraph import PlotWidget, plot
# from random import randint

class Worker(QObject, ):
    """Worker thread"""
    finished = pyqtSignal()
    def __init__(self, cam_handler: CameraHandler):
        self.cam_handler = cam_handler
        super().__init__()

    def update_webcam_list(self):
        """Long-running task."""
        self.cam_handler.refresh_camera_list()
        self.finished.emit()

class Ui(QtWidgets.QMainWindow):
    """Class handling Qt GUI control"""
    def __init__(self, ui_file, connection: tuple[str, int], fullscreen):
        self.connection_details = connection
        self.camera_handler = CameraHandler()
        self.app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(ui_file, self) # Load the .ui file

        self.camera_cbo = [
            self.findChild(QtWidgets.QComboBox, 'input_cbo_1'),
            self.findChild(QtWidgets.QComboBox, 'input_cbo_2')
        ]
        self.refresh_webcam_list()


        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        #self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

#        self.update_plot_data()

        if fullscreen:
            self.showFullScreen()
        self.show()
        self.app.exec()

    def refresh_webcam_list(self):
        """Run a Qthread to check possible webcams and create a list"""
        self.thread = QThread()
        self.worker = Worker(self.camera_handler)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.update_webcam_list)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(
            self.callback_func_update_camera_cbo
        )

    def callback_func_update_camera_cbo(self):
        """Callback function for webcam check thread"""
        for cbo in self.camera_cbo:
            for camera in self.camera_handler.get_camera_list():
                cbo.addItem(self.camera_handler.get_camera_string(camera["id"]))
    #def update_plot_data(self):

