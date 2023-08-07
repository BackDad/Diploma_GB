from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from datetime import datetime


class Add_lesson(QDialog):
    def __init__(self, connection):
        super().__init__()
        self.list_tuple = None
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

            self.list_of_students.addItems([items['firstname'] for items in results])
            self.list_tuple = [[items['firstname'], items['id'], items['cost']] for items in results]
            print(self.list_tuple)

    #
    def send_to(self):
        try:
            query_data = [self.list_tuple[self.list_of_students.currentIndex()][1],  # students_ID
                          self.timeEdit.text(),  # Длительность
                          self.lesson_topic.text(),  # Тема урока
                          # self.payment.isChecked(),  # Проверка оплаты
                          str(datetime.now().date()),  # Дата занятия
                          self.list_tuple[self.list_of_students.currentIndex()][2]
                          ]
            # ______________________________________
            print(query_data)
            for types in range(len(query_data)):
                print(query_data[types], type(query_data[types]))

            # ______________________________________
            with self.connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO lessons (students_id, lesson_date, lesson_duration,lesson_topic,payment)'
                    'VALUES (%s,%s,%s,%s,%s)',
                    (query_data[0],
                     query_data[3],
                     query_data[1],
                     query_data[2],
                     query_data[4]))
                self.connection.commit()
                print("Успешно!")
        except Exception as ex:
            print("Error", ex)
