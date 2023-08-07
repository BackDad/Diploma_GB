from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.uic import loadUi
import pymysql
from PyQt5.QtCore import pyqtSignal


class billForm(QWidget):
    studentSelected = pyqtSignal(int)

    def __init__(self, connection):
        super().__init__()
        self.student_id = None
        self.selected_lesson = None
        self.connection = connection
        loadUi('Interface/Bill.ui', self)
        self.payment_button.clicked.connect(self.send_bill)
        self.list_of_students.currentIndexChanged.connect(self.on_student_selected)
        self.list_of_lesson.currentIndexChanged.connect(self.on_combobox_item_selected)

    def send_bill(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('UPDATE lessons SET payment_bool= %s WHERE students_id=%s and lesson_topic = %s',
                               (True, self.student_id, self.selected_lesson))
                self.connection.commit()
                self.info_lable.setText("Успешно")
                # print(self.lesson_topic)
        except Exception as ex:
            print(ex)
            self.info_lable.setText(ex)

    def list_of_student(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT firstname,id  FROM students ')
            students = cursor.fetchall()
            for student in students:
                self.list_of_students.addItem(student['firstname'], student['id'])

    def list_of_lessons(self, student_id):
        self.list_of_lesson.clear()
        if student_id is not None:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT lesson_date, lesson_topic FROM lessons WHERE students_id = %s AND payment_bool '
                               '= 0  ', student_id)
                lessons = cursor.fetchall()
                for lesson in lessons:
                    self.list_of_lesson.addItem(lesson['lesson_topic'], lesson['lesson_date'])

    def on_student_selected(self, index):

        self.student_id = self.list_of_students.itemData(index)
        self.studentSelected.emit(self.student_id)

    def on_combobox_item_selected(self):
        # Получаем текст выбранного занятия и сохраняем его в атрибут класса
        self.selected_lesson = self.list_of_lesson.currentText()
        print(f"Выбранное занятие: {self.selected_lesson}")
