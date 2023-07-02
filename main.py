import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PyQt5.uic import loadUi


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # Загрузка файла .ui
        loadUi('Assistant.ui', self)
        self.Show_Student_All.clicked.connect(self.Show_student_All_f)
        self.Add_student.clicked.connect(self.Add_student_f)
        self.Show_Student_Active.clicked.connect(self.Show_Student_Active_f)
        self.Del_Student.clicked.connect(self.Del_student_f)

    def Show_student_All_f(self):
        QMessageBox.information(self, "Button Clicked", "Button Show_student_All was clicked!")

    def Add_student_f(self):
        QMessageBox.information(self, "Button Clicked", "Button Add_student was clicked!")

    def Del_student_f(self):
        QMessageBox.information(self, "Button Clicked", "Button Del_student was clicked!")

    def Show_Student_Active_f(self):
        QMessageBox.information(self, "Button Clicked", "Button Show_Student_Active was clicked!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
