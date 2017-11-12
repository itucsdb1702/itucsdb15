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

login_manager = LoginManager()

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
        PRIMARY KEY(ID)
        )"""
        cursor.execute(query)
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