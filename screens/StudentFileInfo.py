from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class StudentInfoDialog(QDialog):
    def __init__(self, student_data):
        try:
            super().__init__()
            loadUi('Interface/StudentInfoDialog.ui', self)
            # print(student_data)
            self.name_l.setText(student_data['Name'])
            self.target_l.setText(student_data['Target'])
            self.contact_l.setText(student_data['Contact'])
            self.cost_l.setText(student_data['Cost'])
            self.Ok_b.clicked.connect(self.close_window)
        except Exception as ex:
            print(ex)

    def close_window(self):
        self.close()
