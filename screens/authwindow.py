import pymysql
from config.config import host, user, password, db_name
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


def connect_to_database(host=host, user=user, password=password,
                        db_name=db_name):
    try:
        print("Йэс")
        return pymysql.connect(
            host=host, port=3306, password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor, user=user
        )
    except Exception as ex:
        print("Ошибка подключения к базе данных:", ex)
        return None


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Interface/Auth.ui", self)
        self.Connect.clicked.connect(self.save_data_to_config())

    def save_data_to_config(self):
        host = self.label_host.text()
        user = self.label_user.text()
        password = self.label_password.text()
        db_name = self.label_db_name.text()

        # Записываем данные в файл config.py
        with open("config/config.py", "w") as file:
            file.write(f"host = '{host}'\n")
            file.write(f"user = '{user}'\n")
            file.write(f"password = '{password}'\n")
            file.write(f"db_name = '{db_name}'\n")
