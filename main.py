import sys
from PyQt5.QtWidgets import QApplication, QDialog
from screens.mainwindow import MainWindow
from screens.authwindow import AuthWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    if auth_window.exec_() == QDialog.Accepted:
        window = MainWindow(auth_window.connection)
        window.show()
        sys.exit(app.exec_())
