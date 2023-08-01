from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView
from PyQt5.uic import loadUi
from screens.deletedialog import DeleteDialog
from screens.addstudentform import AddStudentForm
from screens.StudentFileInfo import StudentInfoDialog
from screens.add_lesson import Add_lesson


class CustomException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.add_lesson_w = None
        self.connection = connection
        self.profile = None
        self.delete_dialog = None
        self.auth_form = None
        self.add_student_form = None
        self.student_data = None
        loadUi('Interface/Draft/New_view.ui', self)
        self.Show_Student_All.clicked.connect(self.show_all_students)
        self.Add_student.clicked.connect(self.open_add_student_form)
        self.Show_Student_Active.clicked.connect(self.add_lesson)
        self.Del_Student.clicked.connect(self.open_delete_dialog)
        self.tableView.clicked.connect(self.show_student_info)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.show_all_students()

    def open_add_student_form(self):
        self.add_student_form = AddStudentForm(self.connection)
        self.add_student_form.show()

    def show_all_students(self):

        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students ')
                results = cursor.fetchall()
                if not results:
                    raise CustomException("База данных пуста!")
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

        except CustomException as ex:

            self.Error_lable.setText(f"Ошибка: {ex}")

    def open_delete_dialog(self):
        self.delete_dialog = DeleteDialog(self.connection)
        self.delete_dialog.show()

    def show_student_info(self, index):
        # Получаем данные об ученике из модели

        row = index.row()
        student_data = {
            "Name": self.model.item(row, 1).text(),
            "Contact": self.model.item(row, 2).text(),
            "Cost": self.model.item(row, 3).text(),
            "Target": self.model.item(row, 4).text(),
            "Date": self.model.item(row, 5).text(),
        }
        self.profile = StudentInfoDialog(student_data)
        self.profile.show()

    def add_lesson(self):
        try:
            self.add_lesson_w = Add_lesson(self.connection)
            self.add_lesson_w.show()
        except Exception as ex:
            print(ex)
