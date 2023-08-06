from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView, QListView
from PyQt5.uic import loadUi
from screens.deletedialog import DeleteDialog
from screens.addstudentform import AddStudentForm
from screens.StudentFileInfo import StudentInfoDialog
from screens.add_lesson import Add_lesson
from datetime import datetime
from PyQt5.QtCore import QTimer, QTime


class CustomException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.results = None
        self.add_lesson_w = None
        self.connection = connection
        self.profile = None
        self.delete_dialog = None
        self.auth_form = None
        self.add_student_form = None
        self.student_data = None
        loadUi('Interface/Draft/New_view.ui', self)
        # self.Show_Student_All.clicked.connect(self.show_all_students) удалена
        self.Add_student.clicked.connect(self.open_add_student_form)
        self.Show_Student_Active.clicked.connect(self.add_lesson)
        self.Del_Student.clicked.connect(self.open_delete_dialog)
        self.tableView.clicked.connect(self.show_student_info)
        self.show_current_lessons()
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.headers = ['ID', 'Ученик', 'Номер \n телефона', 'Гонорар', 'Цель', 'Дата \n начала', 'Первый \n день',
                        'Время \n первого \n  занятия',
                        'Второй \n день', 'Время \n второго \n занятия']
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.delete_dialog = DeleteDialog(self.connection)
        self.delete_dialog.data_updated.connect(self.show_all_students)
        self.add_student_form = AddStudentForm(self.connection)
        self.add_student_form.data_updated.connect(self.show_all_students)

        self.add_student_form.data_updated.connect(self.show_current_lessons)
        self.delete_dialog.data_updated.connect(self.show_current_lessons)
        if self.Tconnection():
            self.show_all_students()

    def open_add_student_form(self):
        self.add_student_form.show()

    def show_all_students(self):

        self.results = self.Tconnection()
        if self.results:
            self.model.clear()
            # Устанавливаем количество строк и столбцов в модели
            self.model.setRowCount(len(self.results))
            self.model.setColumnCount(
                len(self.results[0]))  # Предполагается, что все записи имеют одинаковое количество столбцов

            # Заполняем модель данными из результатов запроса
            for row, result in enumerate(self.results):
                for column, (key, value) in enumerate(result.items()):
                    item = QStandardItem(str(value))
                    self.model.setItem(row, column, item)
            # Устанавливаем заголовки столбцов
            # column_names = list(self.results[0].keys())
            self.model.setHorizontalHeaderLabels(self.headers)  # Разрешаем изменение размеров столбцов и
            # выделение целых строк
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView.setSelectionBehavior(QTableView.SelectRows)
            self.Erro_lable.setText(f"Обновлено {updTime()} ")

        else:
            self.model.clear()
            self.Erro_lable.setText(f"База данных пуста {updTime()}")

    def open_delete_dialog(self):
        if self.Tconnection():
            self.delete_dialog.show()
        else:
            print(f"База данных пуста {updTime()}")
            self.Erro_lable.setText(f"База данных пуста {updTime()}")

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

    def Tconnection(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students ')
        return cursor.fetchall()

    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString('hh:mm:ss')
        self.Time_lable.setText(time_text)

    def show_current_lessons(self):
        weekday_dict = {0: 'ПН',
                        1: 'ВТ',
                        2: 'СР',
                        3: 'ЧТ',
                        4: 'ПТ',
                        5: 'СБ',
                        6: 'ВС'
                        }
        current_time = datetime.now().time()
        current_week = datetime.now().weekday()
        if current_week in weekday_dict:
            self.lesson_lable.setText(str(weekday_dict[current_week]))
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT firstname, target,first_day_time, second_day_time 
                FROM students 
                WHERE (first_day = %s AND first_day_time>=%s) 
                OR 
                (second_day = %s AND second_day_time>=%s)
                 ''',(self.lesson_lable.text(),current_time,self.lesson_lable.text(),current_time,))
            result = cursor.fetchall()
            temp_str = ''
            temp_s = ''
            for item in result:
                temp_str = item['firstname'] + ' ' + item['target'] + ' ' + str(item['first_day_time']) + '\n'
                temp_s += temp_str
            self.lesson_lable.setText(temp_s)


def updTime():
    return f"{datetime.now().time().hour}:" \
           f"{datetime.now().time().minute}:" \
           f"{datetime.now().time().second}"
