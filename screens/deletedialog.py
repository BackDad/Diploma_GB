from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from screens.authwindow import connect_to_database


class DeleteDialog(QDialog):
    def __init__(self):
        try:
            super().__init__()
            loadUi('Interface/Delete_dialog.ui', self)
            self.connection = connect_to_database()
            self.Delete_button.clicked.connect(self.delete_row)
        except Exception as ex:
            print(ex)

    def delete_row(self):
        name = self.Delete_row.text()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students ')
                results = cursor.fetchall()
            if name != "":
                with self.connection.cursor() as cursor:
                    cursor.execute('DELETE FROM Students WHERE firstname = %s LIMIT 1', name)
                    self.connection.commit()
                    self.Delete_error.setText("Запись успешно удалена из БД.")
            else:
                self.Delete_error.setText("Пустой запрос")
        except Exception as ex:
            print(ex)
