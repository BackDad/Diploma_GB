from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from datetime import datetime


class Add_lesson(QDialog):
    def __init__(self, connection):
        super().__init__()
        self.result = None
        self.connection = connection
        loadUi('Interface/Add_lesson.ui', self)
        self.pushButton.clicked.connect(self.send_to)
        self.list_of_student()

    def list_of_student(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students ')
            results = cursor.fetchall()
            self.result = results
            print(results)
            for items in results:
                self.list_of_students.addItems([str((items['firstname'], items['id'], items['cost']))])

    #
    def send_to(self):
        try:
            query_data = [int(self.list_of_students.currentText().split(',')[1]),  # students_ID
                          self.timeEdit.text(),  # Длительность
                          self.lesson_topic.text(),  # Тема урока
                          self.payment.isChecked(),  # Проверка оплаты
                          str(datetime.now().date()),  # Дата занятия
                          int(self.list_of_students.currentText().split(',')[2].replace(')', ''))
                          ]
            # ______________________________________
            print(query_data)
            for types in range(len(query_data)):
                print(type(query_data[types]))
            # ______________________________________
            with self.connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO lessons (students_id, lesson_date, lesson_duration,lesson_topic,payment ,payment_bool)'
                    'VALUES (%s,%s,%s,%s,%s,%s)',
                    (query_data[0], query_data[4],
                     query_data[1], query_data[2],
                     query_data[5], query_data[3]))
                self.connection.commit()
                print("Успешно!")
        except Exception as ex:
            print("Error", ex)
