import mysql.connector
import os
import logging

logging.basicConfig(filename='app.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')


class PasswordsDB:
    def __init__(self):
        self.mydb = None
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
        except Exception as e:
            logging.error(e)

        crs = self.mydb.cursor()
        crs.execute("CREATE DATABASE IF NOT EXISTS password_manager_db")

        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except Exception as e:
            logging.error(e)


        self.cursor = self.mydb.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS passwords (id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT, password_name "
            "VARCHAR(255), login VARCHAR(255), password VARCHAR(255))")

    def add_password(self, user_id, password_name, login, password):
        try:
            sql = "INSERT INTO passwords (user_id, password_name, login, password) VALUES (%s, %s, %s, %s)"
            val = (user_id, password_name, login, password)
            self.cursor.execute(sql, val)
            self.mydb.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def check_password_name(self, user_id, password_name):
        sql = "SELECT * FROM passwords WHERE password_name = %s AND user_id = %s"
        val = (password_name, user_id)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def get_password(self, user_id, password_name):
        sql = "SELECT login, password FROM passwords WHERE user_id=%s AND password_name=%s"
        val = (user_id, password_name)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def delete_password(self, user_id, password_name):
        sql = "DELETE FROM passwords WHERE user_id = %s AND password_name = %s"
        val = (user_id, password_name)
        try:
            self.cursor.execute(sql, val)
            self.mydb.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
