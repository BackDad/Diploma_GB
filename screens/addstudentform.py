from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from screens.authwindow import connect_to_database


class AddStudentForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Interface/Add_student_form.ui', self)
        self.connection = connect_to_database()
        self.Save_button.clicked.connect(self.add_student)

    def add_student(self):
        try:
            query_data = [self.Name.text(), self.Contact.text(), self.Cost.text(), self.Target.text(), self.Date.text()]
            if '' in query_data:
                self.Error_lable.setText("Ошибка: Пустые поля")
                self.check_fields()
            else:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO students (firstname, contact, cost, target, data_add) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (query_data[0], query_data[1], int(query_data[2]), query_data[3], query_data[4])
                    )
                    self.connection.commit()
                    self.Error_lable.setText("Данные успешно добавлены в БД.")
                    self.check_fields()
        except Exception as ex:
            self.Error_lable.setText(f"Ошибка:{ex}")
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
