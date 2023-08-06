import pymysql
# from config.config import host as default_host, user as default_user, password as default_password, \
#     db_name as default_db_name
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Interface/Auth.ui', self)

        self.connection = None
        self.Connect_to_db.clicked.connect(self.auth)
        self.Error_lable.setText('Приветствую!')

    def auth(self):
        host = self.Host_name.text()
        user = self.User_name.text()
        password = self.Pass_value.text()
        db_name = self.DB_name.text()

        connection = self.connect_to_database(host, user, password, db_name)
        if connection:
            self.connection = connection
            self.accept()
        else:
            self.show_error("Ошибка подключения к базе данных.")

    def show_error(self, message):
        # Отображение сообщения об ошибке пользователю
        pass

    def connect_to_database(self, host, user, password, db_name):
        try:
            return pymysql.connect(
                host=host, port=3306, password=password, database=db_name,
                cursorclass=pymysql.cursors.DictCursor, user=user
            )
        except Exception as ex:

            print("Ошибка подключения к базе данных:", ex)
            self.Error_lable.setText(f"Ошибка: {ex}")
            return None
