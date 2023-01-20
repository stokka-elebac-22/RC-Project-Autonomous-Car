"""GUI module."""
import sys
import cv2
from PyQt6 import QtGui, QtCore, QtWidgets

class DisplayImageWidget(QtWidgets.QWidget):
    """Qt widget."""
    def __init__(self, parent=None):
        super(DisplayImageWidget, self).__init__(parent)

        self.button = QtWidgets.QPushButton('Show picture')
        self.button.clicked.connect(self.show_image)
        self.image_frame = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)
        self.image = None

    @QtCore.pyqtSlot()
    def show_image(self):
        """Shows image in frame."""
        self.image = cv2.imread('placeholder4.PNG')
        self.image = QtGui.QImage(self.image.data, self.image.shape[1], \
            self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    display_image_widget = DisplayImageWidget()
    display_image_widget.show()
    sys.exit(app.exec_())
