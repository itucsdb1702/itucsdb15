import requests
import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
from flask import redirect
from flask.helpers import url_for
from flask import Flask, flash
from flask import render_template
from classes import User
from classes import UserList
from flask_login import login_manager
from flask_login.login_manager import LoginManager
from routes import page
from flask_login.utils import current_user
from initialize_db import initialize_db_function


login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
        with dbapi2._connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT EMAIL FROM USERS WHERE (USERNAME = %s)"
            cursor.execute(query, (user_id,))
            email = cursor.fetchone()
            cursor = connection.cursor()
            query = "SELECT PASSWORD FROM USERS WHERE (USERNAME = %s)"
            cursor.execute(query, (user_id,))
            password = cursor.fetchone()

            user = User(user_id, password, email)
            return user

def create_app():
    app = Flask(__name__)
    app.register_blueprint(page)
    app.userlist = UserList()
    app.secret_key = "secret key"
    login_manager.init_app(app)
    login_manager.login_view = 'page.signup'
    return app

app = create_app()



def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/init_user_db')
def init_user_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)

        query = """CREATE TABLE USERS(
        ID SERIAL NOT NULL,
        USERNAME VARCHAR(30),
        PASSWORD VARCHAR(250),
        EMAIL VARCHAR(50),
        POST_ID INTEGER,
        PRIMARY KEY(ID),
        UNIQUE (USERNAME)
        )"""
        cursor.execute(query)
    return redirect(url_for('page.home_page'))

@app.route('/make_username_unique')
def unique_username():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        

        query = """ALTER TABLE USERS
            ADD UNIQUE (USERNAME)
        """
        cursor.execute(query)
    return redirect(url_for('page.home_page'))

@app.route('/init_movies_db')
def init_movies_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "DROP TABLE IF EXISTS MOVIES"
        cursor.execute(query)

        query ="""CREATE TABLE MOVIES(
        MOVIEID SERIAL NOT NULL,
        TITLE VARCHAR(100),
        YEAR INTEGER,
        SCORE FLOAT,
        VOTES INTEGER,
        IMDB_URL VARCHAR(2068),
        PRIMARY KEY(MOVIEID)
        )
        """
        cursor.execute(query)
        connection.commit()

        return redirect(url_for('page.home_page'))



@app.route('/init_posts_db')
def init_posts_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "DROP TABLE IF EXISTS POSTS"
        cursor.execute(query)

        query = """CREATE TABLE POSTS(
        POST_ID SERIAL NOT NULL,
        COMMENTS VARCHAR(300),
        MOVIE_ID INTEGER,
        PRIMARY KEY(POST_ID)
        )
        """
        cursor.execute(query)


        query = """ALTER TABLE POSTS
        ADD FOREIGN KEY(MOVIE_ID)
        REFERENCES MOVIES(MOVIEID)
        ON DELETE CASCADE
        """
        cursor.execute(query)

        connection.commit()

        return redirect(url_for('page.home_page'))

@app.route('/init_watchedlist_db')
def init_watchedlist_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "DROP TABLE IF EXISTS WATCHEDLIST"
        cursor.execute(query)

        query = """CREATE TABLE WATCHEDLIST (USERNAME VARCHAR(30) NOT NULL,
            MOVIEID INT NOT NULL,
            SCORE INT, CONSTRAINT PAIR PRIMARY KEY (USERNAME,MOVIEID),
                FOREIGN KEY (USERNAME) REFERENCES USERS(USERNAME),
                FOREIGN KEY (MOVIEID) REFERENCES MOVIES(MOVIEID)
        )"""
        cursor.execute(query)

        connection.commit()

        return redirect(url_for('page.home_page'))

@app.route('/init_followers_db')    
def init_followers_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "DROP TABLE IF EXISTS FOLLOWERS"
        cursor.execute(query)

        query = """CREATE TABLE FOLLOWERS (FRIENDSHIP_ID SERIAL NOT NULL,
            FOLLOWING_USER_ID INT NOT NULL,
            FOLLOWED_USER_ID INT, CONSTRAINT FRIENDSHIP UNIQUE (FOLLOWING_USER_ID,FOLLOWED_USER_ID),
                FOREIGN KEY (FOLLOWING_USER_ID) REFERENCES USERS(ID),
                FOREIGN KEY (FOLLOWED_USER_ID) REFERENCES USERS(ID)
            ON DELETE CASCADE
        )"""
        cursor.execute(query)

        connection.commit()

        return redirect(url_for('page.home_page'))
@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        initialize_db_function(cursor)
        connection.commit()
    return redirect(url_for('page.home_page'))

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)