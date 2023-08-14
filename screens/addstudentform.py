from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal


class AddStudentForm(QDialog):
    data_updated = pyqtSignal()

    def __init__(self, connection):
        super().__init__()
        loadUi('Interface/Add_student_form.ui', self)
        self.connection = connection
        self.Save_button.clicked.connect(self.add_student)
        self.check2.stateChanged.connect(self.changed)

    def add_student(self):
        try:
            query_data = [self.Name.text(),  # 0
                          self.Contact.text(),  # 1
                          self.Cost.text(),  # 2
                          self.Target.text(),  # 3
                          self.Date.text(),  # 4
                          self.WeekDaybox1.currentText(),  # 5 self.WeekDaybox1.currentIndex() заменил на дни как текст
                          self.WeekDaybox2.currentText(),  # 6 self.WeekDaybox1.currentIndex()
                          self.SecondDayTime.text(),  # 7
                          self.FirstDayTime.text()  # 8
                          ]
            if not self.check2.isChecked():
                query_data[6], query_data[7] = None, None

            print(query_data)
            if '' in query_data:
                self.Error_lable.setText("Ошибка: Пустые поля")
                self.check_fields()

            else:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO students '
                        '(firstname, contact, cost,'
                        ' target, data_add, first_day,first_day_time, second_day,'
                        'second_day_time)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s)',
                        (query_data[0], query_data[1], int(query_data[2]),
                         query_data[3], query_data[4], query_data[5], query_data[8],
                         query_data[6], query_data[7])
                    )
                    self.connection.commit()
                    self.Error_lable.setText("Данные успешно добавлены в БД.")
                    self.data_updated.emit()

                    self.check_fields()
        except Exception as ex:
            self.Error_lable.setText(f"Ошибка:{ex}")
            self.check_fields()

    def check_fields(self):
        style = "background-color: #D3D3D3; border: 2px solid #00CED1; border-radius: 5px;"
        fields = [self.Name, self.Contact, self.Cost, self.Target, self.Date]
        for field in fields:
            if field.text() == "":
                field.setStyleSheet(
                    "background-color: #ff0000; border: 2px solid #00CED1; border-radius: 5px;"
                )
            else:
                field.setStyleSheet(style)

    def changed(self, checked):
        try:
            if checked:
                self.WeekDaybox2.setEnabled(True)
                self.SecondDayTime.setEnabled(True)
            else:
                self.WeekDaybox2.setEnabled(False)
                self.SecondDayTime.setEnabled(False)
        except Exception as ex:
            print(ex)
