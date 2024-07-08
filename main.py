import sys
from MainWindow import MyWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()
