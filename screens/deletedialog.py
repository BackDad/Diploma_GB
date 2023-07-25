from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class DeleteDialog(QDialog):
    def __init__(self, connection):
        super().__init__()
        try:
            loadUi('Interface/Delete_dialog.ui', self)
            self.connection = connection
            self.Delete_button.clicked.connect(self.delete_row)

        except Exception as ex:
            print(ex)

    def delete_row(self):
        id_s = self.Delete_row.text()
        try:
            if id_s != "":
                with self.connection.cursor() as cursor:
                    cursor.execute('DELETE FROM Students WHERE id = %s LIMIT 1', id_s)
                    self.connection.commit()
                    self.Delete_error.setText("Запись успешно удалена из БД.")

                    self.close()
            else:
                self.Delete_error.setText("Пустой запрос")
        except Exception as ex:
            print(ex)
