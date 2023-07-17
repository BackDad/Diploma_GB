from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView
from PyQt5.uic import loadUi
from screens.authwindow import connect_to_database
from screens.deletedialog import DeleteDialog
from screens.addstudentform import AddStudentForm


class CustomException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.delete_dialog = None
        self.auth_form = None
        self.add_student_form = None
        self.connection = None
        loadUi('Interface/Assistant.ui', self)
        self.Show_Student_All.clicked.connect(self.show_all_students)
        self.Add_student.clicked.connect(self.open_add_student_form)
        self.Show_Student_Active.clicked.connect(self.show_active_students)
        self.Del_Student.clicked.connect(self.open_delete_dialog)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

    def open_add_student_form(self):
        self.add_student_form = AddStudentForm()
        self.add_student_form.show()

    def show_all_students(self):

        try:
            self.connection = connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students ')
                results = cursor.fetchall()
                if not results:
                    print(True)
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
        self.delete_dialog = DeleteDialog()
        self.delete_dialog.show()

    def show_active_students(self):
        # Остальной код отображения активных студентов
        pass
