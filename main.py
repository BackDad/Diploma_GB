
import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableView, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from config import host as default_host, user as default_user, password as default_password, db_name as default_db_name


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Auth.ui", self)
        self.Connect_to_db.clicked.connect(self.auth)
        self.connection = None

    def accept(self):
        super().accept()  # Вызвать родительский метод accept()
        return self.connection  # Вернуть значение connection

    def auth(self):
        host = self.Host_name.text() or default_host
        user = self.User_name.text() or default_user
        password = self.Pass_value.text() or default_password
        db_name = self.DB_name.text() or default_db_name

        connection = connect_to_database(host, user, password, db_name)
        if connection:
            self.accept()  # Закрыть окно аутентификации, если соединение успешно
        else:
            self.show_error("Ошибка подключения к базе данных.")

    def show_error(self, message):
        # Отображение сообщения об ошибке пользователю
        pass


def connect_to_database(host=default_host, user=default_user, password=default_password, db_name=default_db_name):
    try:
        return pymysql.connect(
            host=host, port=3306, password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor, user=user
        )
    except Exception as ex:
        print("Ошибка подключения к базе данных:", ex)
        return None


class DeleteDialog(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi('Delete_dialog.ui', self)
        self.connection = connection
        self.Delete_button.clicked.connect(self.delete_row)

    def delete_row(self):
        name = self.Delete_row.text()
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM Students WHERE firstname = %s LIMIT 1', name)
            self.connection.commit()
            self.Delete_error.setText("Запись успешно удалена из БД.")


class AddStudentForm(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi('Add_student_form.ui', self)
        self.connection = connection
        self.Save_button.clicked.connect(self.add_student)

    def add_student(self):
        try:
            query_data = [self.Name.text(), self.Contact.text(), self.Cost.text(), self.Target.text(), self.Date.text()]
            if '' in query_data:
                self.Error_label.setText("Ошибка: Пустые поля")
                self.check_fields()
            else:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO students (firstname, contact, cost, target, data_add) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (query_data[0], query_data[1], int(query_data[2]), query_data[3], query_data[4])
                    )
                    self.connection.commit()
                    self.Error_label.setText("Данные успешно добавлены в БД.")
                    self.check_fields()
        except Exception as ex:
            print("Error:", ex)
            self.check_fields()

    def check_fields(self):
        style = "background-color: qlineargradient(spread:pad, x1:0.573864, y1:0.006, x2:0.551, y2:0.988636," \
                "stop:0.375 rgba(141, 206, 180, 255), stop:1 rgba(255, 255, 255, 255));\nborder-radius: 10px;"
        fields = [self.Name, self.Contact, self.Cost, self.Target, self.Date]
        for field in fields:
            if field.text() == "":
                field.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0.573864, y1:0.006, x2:0.551, y2:0.988636,"
                    "stop:0.375 rgba(255, 0, 0, 255), stop:1 rgba(163, 0, 0, 255));border-radius: 10px"
                )
            else:
                field.setStyleSheet(style)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connection = None
        loadUi('Assistant.ui', self)
        self.Show_Student_All.clicked.connect(self.show_all_students)
        self.Add_student.clicked.connect(self.open_add_student_form)
        self.Show_Student_Active.clicked.connect(self.show_active_students)
        self.Del_Student.clicked.connect(self.open_delete_dialog)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.Connect_to_db.clicked.connect(self.open_auth_window)

    def open_add_student_form(self):
        self.add_student_form = AddStudentForm(self.connection)
        self.add_student_form.show()

    def open_auth_window(self):
        self.auth_form = AuthWindow()
        if self.auth_form.exec_() == QDialog.Accepted:
            self.connection = connect_to_database(
                self.auth_form.Host_name.text(),
                self.auth_form.User_name.text(),
                self.auth_form.Pass_value.text(),
                self.auth_form.DB_name.text()
            )
            if self.connection:
                print("Успешное подключение к базе данных.")
            else:
                print("Ошибка подключения к базе данных.")

    def show_all_students(self):
        try:
            try:
                self.connection = connect_to_database()
            except Exception as ex:
                print(ex)
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
            self.Error_label.setText(f"Ошибка: {ex}")

    def open_delete_dialog(self):
        self.delete_dialog = DeleteDialog(self.connection)
        self.delete_dialog.show()

    def show_active_students(self):
        # TODO: Реализовать функциональность отображения активных студентов
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
