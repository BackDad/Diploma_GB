import pymysql
from config.config import host as default_host, user as default_user, password as default_password, db_name as default_db_name


def connect_to_database(host=default_host, user=default_user, password=default_password, db_name=default_db_name):
    try:
        return pymysql.connect(
            host=host, port=3306, password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor, user=user
        )
    except Exception as ex:
        print("Ошибка подключения к базе данных:", ex)
        return None
