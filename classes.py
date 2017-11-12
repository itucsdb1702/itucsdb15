import psycopg2 as dbapi2
from flask import current_app as app
from flask_login import UserMixin
from flask import flash
from passlib.apps import custom_app_context as pwd_context

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

    def verify(self,username,passw):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT USERNAME, PASSWORD FROM USERS WHERE (NAME = %s)"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user is not None:
                if pwd_context.verify(passw,user[1]):
                    return 0
                else:
                    return -1
            else:
                return -1

