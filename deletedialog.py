from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from authwindow import connect_to_database


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Delete_dialog.ui', self)
        self.connection = connect_to_database()
        self.Delete_button.clicked.connect(self.delete_row)

    def delete_row(self):
        name = self.Delete_row.text()
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM Students WHERE firstname = %s LIMIT 1', name)
            self.connection.commit()
            self.Delete_error.setText("Запись успешно удалена из БД.")
