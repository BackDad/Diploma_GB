import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PyQt5.uic import loadUi
import pymysql
from config import host, user, password, db_name


def Connect_to_db(self):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
            user=user
        )
        self.Result_Area.setText("Successfully Connected...")
        print("Successfully Connected...")
        try:
            cursor = connection.cursor()
            pass
        finally:
            connection.close()
    except Exception as ex:
        print("Connection error")
        self.Result_Area.setText("Connection Error..." + ex)
        print(ex)


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
        new_text = "Button Show_student_All"
        self.Result_Area.setText(new_text)

    def Add_student_f(self):
        new_text = "Button Add_student"
        self.Result_Area.setText(new_text)

    def Del_student_f(self):
        new_text = "Button Del_student"
        self.Result_Area.setText(new_text)

    def Show_Student_Active_f(self):
        new_text = "Button Show_Student_Active"
        self.Result_Area.setText(new_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
