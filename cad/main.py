import sys
from PyQt5.QtWidgets import *

from cad_window import CADWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = CADWindow()

    sys.exit(app.exec_())

