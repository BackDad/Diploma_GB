from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal


class DeleteDialog(QDialog):
    data_updated = pyqtSignal()

    def __init__(self, connection):
        super().__init__()
        self.results = None
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
                    self.Delete_error.setText("Удалено успешно!")
                    self.data_updated.emit()
                    # self.close()
            else:
                self.Delete_error.setText("Пустой запрос или нечего удалять")
        except Exception as ex:
            print(ex)
