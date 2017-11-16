import psycopg2 as dbapi2
from flask import current_app as app
from flask_login import UserMixin
from flask import flash
from flask_login import login_manager, login_user, logout_user
from passlib.apps import custom_app_context as pwd_context
from flask_login.login_manager import LoginManager

class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        with dbapi2._connect(app.config['dsn']) as connection:

            cursor = connection.cursor()

            query = "SELECT ID FROM USERS WHERE (USERNAME = %s)"

            cursor.execute(query, (self.username,))

            user = cursor.fetchone()
            if user is None:
                return
            else:
                return self.username
     
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    

        
    

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
            query = "SELECT USERNAME, PASSWORD FROM USERS WHERE (USERNAME = %s)"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user is not None:
                if pwd_context.verify(passw,user[1]):
                    return 0
                else:
                    return -1
            else:
                return -1

