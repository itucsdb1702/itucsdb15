import psycopg2 as dbapi2
from flask import current_app as app
from flask_login import UserMixin
from flask import flash

class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
         with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT ID FROM USERS WHERE (USERNAME = %s)"
            cursor.execute(query, (self.username,))
            user = cursor.fetchone()
            return user

class UserList:
    def __init__(self):
        self.last_user_id = None

    def add_user(self,newuser):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (%s, %s, %s)"""
            cursor.execute(query, (newuser.username, newuser.email, newuser.password))
            connection.commit()
            cursor.close()


