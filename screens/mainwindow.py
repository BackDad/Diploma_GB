from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView, QListView, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.uic import loadUi
from screens.deletedialog import DeleteDialog
from screens.addstudentform import AddStudentForm
from screens.StudentFileInfo import StudentInfoDialog
from screens.billForm import billForm
from screens.add_lesson import Add_lesson
from screens.updatestudentform import UpdateStudentForm
from datetime import datetime
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QColor


class CustomException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class MainWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.bill_form = None
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
        self.Add_bill.clicked.connect(self.open_bill_form)
        self.show_current_lessons()
        self.model = QStandardItemModel()
        self.model_dolg = QStandardItemModel()
        self.model_all_without = QStandardItemModel()
        self.model_lessons = QStandardItemModel()
        self.tableView_3.setModel(self.model_lessons)
        self.tableView.setModel(self.model)
        self.tableView_2.setModel(self.model_dolg)
        self.model_dolg.dataChanged.connect(self.updateCellText)
        self.Update_studen.clicked.connect(self.open_update_student_form)

        self.tableView_4.setModel(self.model_all_without)
        self.tableView_4.selectionModel().selectionChanged.connect(self.show_lessons)
        self.headers = ['ID', 'Ученик', 'Номер \n телефона', 'Гонорар', 'Цель', 'Дата \n начала', 'Первый \n день',
                        'Время \n первого \n  занятия',
                        'Второй \n день', 'Время \n второго \n занятия']

        self.headers_2 = ['Ученик', 'Тема занятия', 'Дата занятия', 'Статус оплаты']
        self.headers_w = ['ID', 'Имя', 'Цель']
        self.headers_lesson = ['Тема', 'Дата']

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.delete_dialog = DeleteDialog(self.connection)
        self.delete_dialog.data_updated.connect(self.show_all_students)
        self.delete_dialog.data_updated.connect(self.show_current_lessons)
        self.add_student_form = AddStudentForm(self.connection)
        self.update_student_form = UpdateStudentForm(self.connection)
        self.add_student_form.data_updated.connect(self.show_all_students)
        self.add_student_form.data_updated.connect(self.show_students)
        self.add_student_form.data_updated.connect(self.show_current_lessons)
        self.update_student_form.data_updated.connect(self.show_all_students)
        self.bill_form = billForm(self.connection)
        self.bill_form.list_of_student()
        self.bill_form.studentSelected.connect(self.bill_form.list_of_lessons)

        self.bill_form.data_updated.connect(self.show_payed_lessons)
        self.add_lesson_w = Add_lesson(self.connection, self.bill_form)

        # self.add_student_form.data_updated.connect(self.add_lesson_w.list_of_student)
        self.add_lesson_w.data_updated.connect(self.show_payed_lessons)

        if self.Tconnection():
            self.show_all_students()

        self.show_payed_lessons()
        self.show_students()
        self.show_lessons()

    def open_add_student_form(self):

        self.add_student_form.show()

    def open_update_student_form(self):
        self.update_student_form.show()
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

    def open_bill_form(self):
        self.bill_form.show()

    # TODO: переработать вывод профайла
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

    # TODO: Убрать try exept
    def add_lesson(self):
        try:
            self.add_lesson_w.show()
        except Exception as ex:
            print(ex)

    # TODO: Переработать передачу подключения к БД
    def Tconnection(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students ')
        return cursor.fetchall()

    # TODO: Переопределить через втроенные методы
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
                 ''', (self.lesson_lable.text(), current_time, self.lesson_lable.text(), current_time,))
            result = cursor.fetchall()
            temp_s = ''
            for item in result:
                temp_str = item['firstname'] + ' ' + item['target'] + ' ' + str(item['first_day_time']) + '\n'
                temp_s += temp_str
            self.lesson_lable.setText(temp_s)

    def show_payed_lessons(self):

        with self.connection.cursor() as cursor:
            # cursor.execute( 'SELECT students.id, students.firstname,students.cost FROM students JOIN lessons ON
            # students.id = lessons.students_id WHERE lessons.payment_bool = 0')
            cursor.execute(
                'SELECT students.firstname, lessons.lesson_topic, lessons.lesson_date,lessons.payment_bool FROM '
                'students INNER JOIN lessons ON students.id = lessons.students_id')
            results = cursor.fetchall()
            print(results)
            if self.results:
                try:
                    self.model_dolg.clear()  # Устанавливаем количество строк и столбцов в модели
                    self.model_dolg.setRowCount(len(results))
                    self.model_dolg.setColumnCount(
                        len(results[0]))  # Предполагается, что все записи имеют одинаковое количество столбцов
                    # Заполняем модель данными из результатов запроса
                    for row, result in enumerate(results):
                        for column, (key, value) in enumerate(result.items()):
                            item = QStandardItem(str(value))
                            self.model_dolg.setItem(row, column, item)
                        # Устанавливаем заголовки столбцов
                        # column_names = list(self.results[0].keys())
                        self.model_dolg.setHorizontalHeaderLabels(self.headers_2)
                        # Разрешаем изменение размеров столбцов и
                        # выделение целых строк
                        self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                        self.tableView_2.setSelectionBehavior(QTableView.SelectRows)
                        # self. Erro_lable_2.setText(f"Обновлено {updTime()} ")
                except Exception as ex:
                    print(ex)

    def show_students(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT id,firstname, target FROM students ')
        results = cursor.fetchall()
        if results:
            self.model_all_without.clear()
            # Устанавливаем количество строк и столбцов в модели
            self.model_all_without.setRowCount(len(results))
            self.model_all_without.setColumnCount(
                len(results[0]))  # Предполагается, что все записи имеют одинаковое количество столбцов

            # Заполняем модель данными из результатов запроса
            for row, result in enumerate(results):
                for column, (key, value) in enumerate(result.items()):
                    item = QStandardItem(str(value))
                    self.model_all_without.setItem(row, column, item)
            # Устанавливаем заголовки столбцов
            # column_names = list(self.results[0].keys())
            self.model_all_without.setHorizontalHeaderLabels(self.headers_w)  # Разрешаем изменение размеров столбцов и
            # выделение целых строк
            self.tableView_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView_4.setSelectionBehavior(QTableView.SelectRows)
            # self.Erro_lable.setText(f"Обновлено {updTime()} ")

        # else:
        # self.model.clear()
        # self.Erro_lable.setText(f"База данных пуста {updTime()}")

    def updateCellText(self, topLeftIndex, bottomRightIndex):
        try:
            for row in range(topLeftIndex.row(), bottomRightIndex.row() + 1):
                for col in range(topLeftIndex.column(), bottomRightIndex.column() + 1):
                    index = self.model_dolg.index(row, col)
                    value = self.model_dolg.data(index, Qt.DisplayRole)
                    if value == "0":
                        self.model_dolg.setData(index, "Не оплачено", Qt.DisplayRole)
                        self.model_dolg.setData(index, Qt.red, Qt.TextColorRole)
                        self.model_dolg.setData(index, QColor('#FFF023'), Qt.BackgroundRole)
                    elif value == '1':
                        self.model_dolg.setData(index, "Оплачено", Qt.DisplayRole)
                        self.model_dolg.setData(index, Qt.green, Qt.TextColorRole)
                        self.model_dolg.setData(index, Qt.white, Qt.BackgroundRole)
        except Exception as ex:
            print(ex)

    def show_lessons(self):
        selected_rows = self.tableView_4.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0]
            student_id = self.tableView_4.model().index(selected_row.row(), 0).data()
            print(student_id)
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT lesson_topic,lesson_date FROM lessons WHERE students_id = %s ', student_id)
            results = cursor.fetchall()
            if results:
                self.model_lessons.clear()
                # Устанавливаем количество строк и столбцов в модели
                self.model_lessons.setRowCount(len(results))
                self.model_lessons.setColumnCount(
                    len(results[0]))  # Предполагается, что все записи имеют одинаковое количество столбцов
                # Заполняем модель данными из результатов запроса
                for row, result in enumerate(results):
                    for column, (key, value) in enumerate(result.items()):
                        item = QStandardItem(str(value))
                        self.model_lessons.setItem(row, column, item)

                self.model_lessons.setHorizontalHeaderLabels(
                    self.headers_lesson)  # Разрешаем изменение размеров столбцов и
                # выделение целых строк
                self.tableView_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tableView_3.setSelectionBehavior(QTableView.SelectRows)
                # self.Erro_lable.setText(f"Обновлено {updTime()} ")
            else:
                self.model_lessons.clear()
                # Устанавливаем заголовки столбцов
                # column_names= list(self.results[0].keys())


# TODO: переопределить через стандартные методы
def updTime():
    return f"{datetime.now().time().hour}:" \
           f"{datetime.now().time().minute}:" \
           f"{datetime.now().time().second}"
