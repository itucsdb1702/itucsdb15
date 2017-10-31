import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
from flask.helpers import url_for
from flask import Flask
from flask import render_template, Response
from flask import request, current_app
from flask import current_app as app
from classes import User
from classes import UserList
from flask_login import login_manager, login_user, logout_user

page = Blueprint('page',__name__)


@page.route('/')
def home_page():
    return render_template('home.html')

@page.route('/home')
def home_page_1():
    return render_template('home.html')

@page.route('/login', methods = ['GET', 'POST'])
def login_page():
    return render_template('login.html')

@page.route('/signup', methods = ['GET', 'POST'])
def signup():
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            with dbapi2._connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = "SELECT ID FROM USERS WHERE (USERNAME = %s)"
                cursor.execute(query, (username,))
                user1 = cursor.fetchone()
                query = "SELECT ID FROM USERS WHERE (EMAIL =%s)"
                cursor.execute(query,(email,))
                user2 = cursor.fetchone()
                if user1 is not None or user2 is not None:
                    if user1 is not None:
                        flash('Please choose a unique Username')
                    if user2 is not None:
                        flash('Please choose a unique E-mail.')
                    return redirect(url_for('page.signup'))
                else:
                    newuser = User(username, email, password)
                    app.userlist.add_user(newuser)
                    return render_template('home.html')
        else:
            return render_template('signup.html')


