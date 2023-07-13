from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView
from PyQt5.uic import loadUi
from authwindow import connect_to_database
from deletedialog import DeleteDialog
from addstudentform import AddStudentForm


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.delete_dialog = None
        self.auth_form = None
        self.add_student_form = None
        self.connection = None
        loadUi('Assistant.ui', self)
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
        self.delete_dialog = DeleteDialog()
        self.delete_dialog.show()

    def show_active_students(self):
        # Остальной код отображения активных студентов
        pass
