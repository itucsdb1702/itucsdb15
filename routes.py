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
from passlib.apps import custom_app_context as pwd_context
from flask_login.utils import current_user
from psycopg2.psycopg1 import connection
from _sqlite3 import connect


page = Blueprint('page',__name__)

@page.route('/')
def home_page():
    return render_template('home.html')

@page.route('/home')
def home_page_1():
    return render_template('home.html')

@page.route('/login', methods = ['GET', 'POST'])
def login_page():

    if request.method == "POST":

        if current_user.get_id() is not None:
            flash('You are already logged in MovieShake as ' + current_user.get_id())
            return redirect(url_for('page.home_page'))
        else:

            username = request.form['uname']
            passwordNotEncrypted = request.form['pass']

            if app.userlist.verify(username, passwordNotEncrypted) is not 0:
                flash('Please check your user name and password')
                return redirect(url_for('page.login_page'))
            else:
                with dbapi2._connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = "SELECT EMAIL FROM USERS WHERE (USERNAME = %s)"
                    cursor.execute(query, (username,))
                    email = cursor.fetchone()


                userToLogin = User(username, email, passwordNotEncrypted)

                if login_user(userToLogin):
                    flash("Welcome, " + current_user.username)
                else:
                    flash("A problem occured, please try again.")

                return redirect(url_for('page.home_page'))

    else:
        return render_template('login.html')


@page.route("/logout")
def logout():
    if current_user.get_id() is not None:
        if logout_user():
            flash("Successfully logged out.")
        else:
            flash("Please try logging out again.")
    else:
        flash("You're not logged in.")

    return redirect(url_for('page.home_page'))


@page.route('/signup', methods = ['GET', 'POST'])
def signup():
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password0 = request.form['password']

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
                    password = pwd_context.encrypt(password0)
                    newuser = User(username, email, password)
                    app.userlist.add_user(newuser)
                    return render_template('home.html')
        else:
            return render_template('signup.html')

@page.route('/actors', methods = ['GET', 'POST'])
def actors():

    stars = []
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM ACTORS"""

        cursor.execute(query)

        for star in cursor:
            stars.append(star)

        connection.commit()


    return render_template('actors.html', stars = stars)


@page.route('/add_actor', methods = ['GET', 'POST'])
def add_actor():

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()


    if request.method == 'POST':
        NAME = request.form['NAME']
        SURNAME = request.form['SURNAME']
        GENDER = request.form['GENDER']
        BIRTHDATE = request.form['BIRTHDATE']
        COUNTRY = request.form['COUNTRY']


        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY))
            connection.commit()

    return redirect('actors')

@page.route('/update_actor', methods = ['GET', 'POST'])
def update_actor():

    if request.method =='POST':
        ID = request.form['ID']
        new_NAME = request.form['N_NAME']
        new_SURNAME = request.form['N_SURNAME']
        new_GENDER = request.form['N_GENDER']
        new_BIRTHDATE = request.form['N_BIRTHDATE']
        new_COUNTRY = request.form['N_COUNTRY']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE ACTORS SET( NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) = ( %s, %s, %s, %s, %s) WHERE ID = %s"""

            cursor.execute(query, (new_NAME, new_SURNAME, new_GENDER, new_BIRTHDATE, new_COUNTRY, ID))
            connection.commit()


    return redirect('actors')

@page.route('/delete_actor', methods = ['GET', 'POST'])
def delete_actor():

    if request.method =='POST':
        ID = request.form['ID']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM ACTORS WHERE ID = '""" +ID + """' """
            cursor.execute(query)
            connection.commit()

    return redirect('actors')
