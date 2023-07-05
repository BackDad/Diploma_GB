# *******************************************************************Refactored*********************************
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableView, QHeaderView
from PyQt5.uic import loadUi
import pymysql
from config import host, user, password, db_name
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Delete_dialog.ui', self)
        self.Delete_button.clicked.connect(self.deleteRow)

    def deleteRow(self):
        name = self.Delete_row.text()
        with pymysql.connect(host=host, port=3306, password=password, database=db_name,
                             cursorclass=pymysql.cursors.DictCursor, user=user) as connection:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM Students WHERE firstname= %s LIMIT 1', name)
                connection.commit()
                self.Delete_error.setText("Запись успешно удалена из БД.")
                print("Запись успешно удалена из БД.")


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Add_student_form.ui', self)
        self.Save_button.clicked.connect(self.addStudent)
        self.connection = pymysql.connect(host=host, port=3306, password=password, database=db_name,
                                          cursorclass=pymysql.cursors.DictCursor, user=user)

    def addStudent(self):
        try:
            query_data = [self.Name.text(), self.Contact.text(), self.Cost.text(), self.Target.text(), self.Date.text()]
            if '' in query_data:
                self.Error_lable.setText("Ошибка: Пустые поля")
                self.checkFields()
            else:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO students (firstname,contact,cost,target,data_add) VALUES (%s,%s,%s,%s,%s)',
                        (query_data[0], query_data[1], int(query_data[2]), query_data[3], query_data[4]))
                    self.connection.commit()
                    self.Error_lable.setText("Данные успешно добавлены в БД.")
                    print("Данные успешно добавлены в БД.")
                    self.checkFields()
        except Exception as ex:
            print("Error.")
            print(ex)
            self.checkFields()

    def checkFields(self):
        style = "background-color: qlineargradient(spread:pad, x1:0.573864, y1:0.006, x2:0.551, y2:0.988636," \
                "stop:0.375 rgba(141, 206, 180, 255), stop:1 rgba(255, 255, 255, 255));\nborder-radius: 10px;"
        fields = [self.Name, self.Contact, self.Cost, self.Target, self.Date]
        for field in fields:
            if field.text() == "":
                field.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0.573864, y1:0.006, x2:0.551, y2:0.988636,"
                    "stop:0.375 rgba(255, 0, 0, 255), stop:1 rgba(163, 0, 0, 255));border-radius: 10px")
            else:
                field.setStyleSheet(style)


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.connection = None
        loadUi('Assistant.ui', self)
        self.Show_Student_All.clicked.connect(self.showAllStudents)
        self.Add_student.clicked.connect(self.openDialog)
        self.Show_Student_Active.clicked.connect(self.showActiveStudents)
        self.Del_Student.clicked.connect(self.openDeleteDialog)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

    def openDialog(self):
        self.dialog = MyForm()
        self.dialog.show()

    def showAllStudents(self):
        try:
            self.connection = pymysql.connect(host=host, port=3306, password=password, database=db_name,
                                              cursorclass=pymysql.cursors.DictCursor, user=user)
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students ')
                results = cursor.fetchall()

            self.model.clear()

            # Устанавливаем количество строк и столбцов в модели
            self.model.setRowCount(len(results))
            self.model.setColumnCount(
                len(results[0]))  # Предполагается, что все записи имеют одинаковое количество столбцов

            # Заполняем модель данными из результатов запроса
            for row, result in enumerate(results):
                for column, (key, value) in enumerate(result.items()):
                    item = QStandardItem(str(value))
                    self.model.setItem(row, column, item)

            # Устанавливаем заголовки столбцов
            column_names = list(results[0].keys())
            self.model.setHorizontalHeaderLabels(column_names)

            # Разрешаем изменение размеров столбцов и выделение целых строк
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView.setSelectionBehavior(QTableView.SelectRows)

        except Exception as ex:
            print("Ошибка при получении данных из базы данных.")
            print(ex)

    def openDeleteDialog(self):
        self.dialog1 = DeleteDialog()
        self.dialog1.show()

    def showActiveStudents(self):
        # TODO: Implement the functionality to show active students
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
