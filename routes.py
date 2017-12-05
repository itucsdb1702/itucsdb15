import datetime
import string
import requests
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
from classes import Movie
from classes import Post
from classes import WatchedList
from classes import FollowerPair
from flask_login import login_manager, login_user, logout_user
from passlib.apps import custom_app_context as pwd_context
from flask_login.utils import current_user
from psycopg2.psycopg1 import connection
from _sqlite3 import connect
from multiprocessing import current_process


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
            flash('You are already logged in MovieShake as ' + current_user.username)
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

    return redirect(url_for('page.login_page'))

@page.route("/edit_profile", methods = ['GET', 'POST'])
def edit_profile():
    if request.method == "GET":
        if current_user.get_id() is not None:
            return render_template('edit.html')
        else:
            flash("You're not logged in.")
            return redirect(url_for('page.login_page'))
    else:
        if current_user.get_id() is not None:
            new_username = request.form['username']
            new_email = request.form['email']
            new_password = request.form['password']

            with dbapi2._connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = "SELECT ID FROM USERS WHERE (USERNAME = %s)"
                cursor.execute(query, (new_username,))
                user1 = cursor.fetchone()
                query = "SELECT ID FROM USERS WHERE (EMAIL =%s)"
                cursor.execute(query,(new_email,))
                user2 = cursor.fetchone()
                if user1 is not None or user2 is not None:
                    if user1 is not None:
                        flash('Please choose a unique Username')
                    if user2 is not None:
                        flash('Please choose a unique E-mail.')
                    return redirect(url_for('page.edit_profile'))

            new_password_encrypted = pwd_context.encrypt(new_password)

            with dbapi2.connect(app.config['dsn']) as connection:
                       cursor = connection.cursor()
                       query = """UPDATE USERS
                                SET USERNAME = %s, EMAIL = %s, PASSWORD = %s
                                WHERE USERNAME = %s;"""

                       cursor.execute(query, (new_username, new_email, new_password_encrypted,current_user.username))
                       connection.commit()
            return redirect(url_for('page.home_page'))
        else:
            flash("You're not logged in.")
            return redirect(url_for('page.login_page'))

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

@page.route('/movies', methods = ['GET', 'POST'])
def movies_page():

    if request.method == "POST":
        movie = Movie(request.form['title'].title(), "", "", "", "")
        score = request.form['score']
        comments = request.form['comment']

        if int(score)<1 or int(score)>10:
            flash("Your rating to the movie should be between 1 and 10.")
            return redirect(url_for('page.movies_page'))

        #checks if user is logged in
        if current_user.get_id() is not None:

            if(movie.search_movie_in_db() != -1):
                movieId = movie.search_movie_in_db()
                userMoviePair = WatchedList(current_user.username, movieId, score)
                post = Post(current_user.get_user_id(), movieId,comments)

                if (userMoviePair.existsInWatchedList() is True):
                    flash("You have already added "+ movie.title+".")
                    return redirect(url_for('page.home_page'))

                else:
                    userMoviePair.add_movie_user_pair()

                    #score and vote need to be updated on movies table
                    oldscore = int(movie.getscore_in_movie_db(movieId)[0])
                    totalVotes = int(movie.getvotes_in_movie_db(movieId)[0])

                    newscore = ((oldscore*totalVotes)+int(score))/(totalVotes + 1)
                    totalVotes = totalVotes + 1

                    movie.update_votes_and_score(movieId, newscore, totalVotes)

                    post.add_post_to_db()
                    flash(movie.title + " is added to your watched list and your post has been saved.")
                    return redirect(url_for('page.home_page'))


            else:
                movieToAdd = movie.verify_movie_from_api()
                if (movieToAdd == -1):
                    flash("There is no such movie")
                    return redirect(url_for('page.home_page'))
                else:
                    movieToAdd = movie.verify_movie_from_api()
                    movieToAdd.score = score

                    movieToAdd.add_movie_to_db()

                    flash(movieToAdd.title + " ("+ movieToAdd.year+") is added to your watched list and your post has been saved.")

                    movieId = movieToAdd.search_movie_in_db()
                    userMoviePair = WatchedList(current_user.username, movieId, score)
                    userMoviePair.add_movie_user_pair()

                    post = Post(current_user.get_user_id(), movieId,comments)
                    post.add_post_to_db()

                    return redirect(url_for('page.home_page'))

        else:
            flash("Please log in to MovieShake")
            return redirect(url_for('page.login_page'))
    else:
        if current_user.get_id() is not None:
            return render_template('movies.html')
        else:
            flash("Please log in to MovieShake")
            return redirect(url_for('page.login_page'))

@page.route("/profile")
def profile_page():

    if current_user.get_id() is not None:
         movies = []
         with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT TITLE, YEAR, m.SCORE, VOTES, IMDB_URL FROM MOVIES m
                                 INNER JOIN WATCHEDLIST w ON (m.MOVIEID = w.MOVIEID)
                                 WHERE (w.USERNAME = %s) """

            cursor.execute(query, (current_user.username, ))

            for movie in cursor:
                movies.append(movie)

            connection.commit()
         return render_template('profile.html', movies = movies)
    else:
        flash("Please log in to MovieShake")
        return redirect(url_for('page.login_page'))


@page.route("/userlist", methods = ['GET', 'POST'])
def UserList():

        users = []
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ID, USERNAME, EMAIL FROM USERS"""

            cursor.execute(query)

            for user in cursor:
                if current_user.username == user[1]:
                    continue
                else:
                    users.append(user)

            connection.commit()
        return render_template('userlist.html', users = users)

@page.route("/follow/<id>")
def Follow(id):
    user = User(current_user.username, "","")
    followingid = user.get_user_id()

    follower_pair = FollowerPair(followingid, id)

    if follower_pair.exists():
        flash('You have already followed that user.')
        return redirect(url_for('page.home_page'))
    else:
        follower_pair.new_follow()
        return redirect(url_for('page.home_page'))


@page.route("/unfollow/<id>")
def Unfollow(id):
    user = User(current_user.username, "","")
    followingid = user.get_user_id()

    follower_pair = FollowerPair(followingid, id)

    if follower_pair.exists() is False:
        flash('You do not follow that user.')
        return redirect(url_for('page.home_page'))
    else:
        follower_pair.unfollow()
        return redirect(url_for('page.home_page'))
