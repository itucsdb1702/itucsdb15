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
from classes import MovieList
from flask_login import login_manager, login_user, logout_user
from passlib.apps import custom_app_context as pwd_context
from flask_login.utils import current_user
from psycopg2.psycopg1 import connection
from _sqlite3 import connect
from multiprocessing import current_process


page = Blueprint('page',__name__)

@page.route('/')
def home_page():
    if current_user.get_id() is None:
        return render_template('home2.html')
    else:
        current_userid = current_user.get_user_id()[0]
        lists = []

        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT DISTINCT m.LIST_NAME, m.USER_ID, u.USERNAME FROM MOVIELIST m
                        INNER JOIN FOLLOWERS f ON (m.USER_ID = f.FOLLOWED_USER_ID)
                        INNER JOIN USERS u ON(u.ID = m.USER_ID)
                        WHERE (f.FOLLOWING_USER_ID = %s)"""

            cursor.execute(query, (current_userid, ))

            for list in cursor:
                lists.append(list[0:3])

            query = """SELECT u.USERNAME FROM USERS u
                        INNER JOIN FOLLOWERS f ON (u.ID = f.FOLLOWED_USER_ID)
                        WHERE(FOLLOWING_USER_ID = %s)"""

            cursor.execute(query, (current_userid, ))

            followings = []
            for following in cursor:
                followings.append(following[0])


            watcheds = []
            for followed in followings:
                query = """SELECT w.USERNAME, m.TITLE, m.IMDB_URL, w.SCORE FROM WATCHEDLIST w
                        INNER JOIN USERS u ON (u.USERNAME = w.USERNAME)
                        INNER JOIN MOVIES m ON (m.MOVIEID = w.MOVIEID)
                        WHERE (w.USERNAME = %s)
                        ORDER BY w.MOVIEID DESC"""

                cursor.execute(query, (followed, ))
                for watched in cursor:
                    watcheds.append(watched[0:4])


        return render_template('home.html', lists = lists, watcheds = watcheds)

@page.route('/home')
def home_page_1():
    if current_user.get_id() is None:
        return render_template('home2.html')
    else:
        current_userid = current_user.get_user_id()[0]
        lists = []

        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT DISTINCT m.LIST_NAME, m.USER_ID, u.USERNAME FROM MOVIELIST m
                        INNER JOIN FOLLOWERS f ON (m.USER_ID = f.FOLLOWED_USER_ID)
                        INNER JOIN USERS u ON(u.ID = m.USER_ID)
                        WHERE (f.FOLLOWING_USER_ID = %s)"""

            cursor.execute(query, (current_userid, ))

            for list in cursor:
                lists.append(list[0:3])

            query = """SELECT u.USERNAME FROM USERS u
                        INNER JOIN FOLLOWERS f ON (u.ID = f.FOLLOWED_USER_ID)
                        WHERE(FOLLOWING_USER_ID = %s)"""

            cursor.execute(query, (current_userid, ))

            followings = []
            for following in cursor:
                followings.append(following[0])


            watcheds = []
            for followed in followings:
                query = """SELECT w.USERNAME, m.TITLE, m.IMDB_URL, w.SCORE FROM WATCHEDLIST w
                        INNER JOIN USERS u ON (u.USERNAME = w.USERNAME)
                        INNER JOIN MOVIES m ON (m.MOVIEID = w.MOVIEID)
                        WHERE (w.USERNAME = %s)
                        ORDER BY w.MOVIEID DESC"""

                cursor.execute(query, (followed, ))
                for watched in cursor:
                    watcheds.append(watched[0:4])


        return render_template('home.html', lists = lists, watcheds = watcheds)

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

                    if login_user(newuser):
                        flash("Welcome, " + current_user.username)
                    else:
                        flash("A problem occured.")

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
    #checks if user is logged in
    if current_user.get_id() is not None:
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
    else:
         flash("Please log in to MovieShake")
         return redirect(url_for('page.login_page'))

@page.route('/update_actor', methods = ['GET', 'POST'])
def update_actor():
    #checks if user is logged in
    if current_user.get_id() is not None:
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
    else:
         flash("Please log in to MovieShake")
         return redirect(url_for('page.login_page'))

@page.route('/delete_actor', methods = ['GET', 'POST'])
def delete_actor():
    #checks if user is logged in
    if current_user.get_id() is not None:
        if request.method =='POST':
             ID = request.form['ID']

             with dbapi2.connect(app.config['dsn']) as connection:
                 cursor = connection.cursor()
                 query = """DELETE FROM ACTORS WHERE ID = '""" + ID + """' """
                 cursor.execute(query)
                 connection.commit()

        return redirect('actors')
    else:
         flash("Please log in to MovieShake")
         return redirect(url_for('page.login_page'))

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

                oldscore = userMoviePair.existsInWatchedList()

                if (oldscore != -1):
                    oldscore = oldscore[0]
                    if int(oldscore) == int(score):
                        flash("You have already added "+ movie.title+".")
                        return redirect(url_for('page.home_page'))
                    else:
                        userMoviePair.updateScoreOfWatchedMovie()


                        oldScoreMoviesTable = int(movie.getscore_in_movie_db(movieId)[0])
                        totalVotes = int(movie.getvotes_in_movie_db(movieId)[0])

                        newscore = ((oldScoreMoviesTable*totalVotes)-int(oldscore)+int(score))/(totalVotes)

                        movie.update_votes_and_score(movieId, newscore, totalVotes)

                        flash("You score to "+ movie.title+" is updated as " + score+".")
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
         lists = []
         userid = current_user.get_user_id()

         with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT TITLE, YEAR, m.SCORE, VOTES, IMDB_URL, m.MOVIEID FROM MOVIES m
                                 INNER JOIN WATCHEDLIST w ON (m.MOVIEID = w.MOVIEID)
                                 WHERE (w.USERNAME = %s) """

            cursor.execute(query, (current_user.username, ))

            for movie in cursor:
                movies.append(movie)

            query = """SELECT DISTINCT LIST_NAME FROM MOVIELIST WHERE (USER_ID = %s)"""

            cursor.execute(query, (userid, ))

            for list in cursor:
                lists.append(list[0])

            followingusers = []
            followingusers = current_user.get_following_users_by_userid()

            posts = []
            posts = current_user.get_posts()

            connection.commit()
            usernames = []
            usernames.append(current_user.username)
         return render_template('profile.html', lists = lists, movies = movies, posts = posts, followingusers = followingusers,
                                username = usernames)
    else:
        flash("Please log in to MovieShake")
        return redirect(url_for('page.login_page'))

@page.route("/userlist", methods = ['GET', 'POST'])
def UserList():
        userid = current_user.get_user_id()
        users = []
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ID, USERNAME, EMAIL FROM USERS

                        EXCEPT

                        SELECT ID, USERNAME, EMAIL FROM USERS u
                        INNER JOIN FOLLOWERS f ON (u.ID = f.FOLLOWED_USER_ID)
                        WHERE (f.FOLLOWING_USER_ID = %s) """

            cursor.execute(query, (userid,))

            for user in cursor:
                if current_user.username == user[1]:
                    continue
                else:
                    users.append(user)

            connection.commit()
        return render_template('userlist.html', users = users)

@page.route("/feed", methods = ['GET', 'POST'])
def feed():
    current_userid = current_user.get_user_id()[0]
    with dbapi2._connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT u.USERNAME FROM USERS u
                        INNER JOIN FOLLOWERS f ON (u.ID = f.FOLLOWED_USER_ID)
                        WHERE(FOLLOWING_USER_ID = %s)"""

        cursor.execute(query, (current_userid, ))

        followings = []
        for following in cursor:
            followings.append(following[0])

        posts = []
        for followed in followings:
            query = """SELECT u.ID, u.USERNAME, m.IMDB_URL, m.TITLE, p.COMMENTS FROM
                            USERS u INNER JOIN POSTS p ON (u.ID = p.USER_ID)

                                    INNER JOIN MOVIES m ON (m.MOVIEID = p.MOVIE_ID)

                        WHERE (USERNAME = %s)

                        ORDER BY p.POST_ID DESC"""

            cursor.execute(query, (followed, ))
            for post in cursor:
                posts.append(post[0:5])

    return render_template('feed.html', posts=posts)

@page.route("/deleteaccount")
def deleteaccount():
    current_userid = current_user.get_user_id()
    if current_userid is not None:
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM USERS WHERE (ID = %s)"""
            cursor.execute(query, current_userid)
            connection.commit()
        return redirect(url_for('page.home_page'))
    else:
        flash("Please log in to MovieShake.")
        return redirect(url_for('page.home_page'))

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

@page.route("/deletepost/<postid>")
def delete_post(postid):
     with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT u.ID, m.MOVIEID, COMMENTS FROM
                            USERS u INNER JOIN POSTS p ON (u.ID = p.USER_ID)
                            INNER JOIN MOVIES m ON (m.MOVIEID = p.MOVIE_ID)
                        WHERE (p.POST_ID = %s)"""

            cursor.execute(query, (postid,))

            post = cursor.fetchone()
            post_to_delete = Post(post[0], post[1],post[2])
            post_to_delete.delete_post_from_db()
            connection.commit()
            return redirect(url_for('page.profile_page'))

@page.route("/updatepost/<postid>", methods = ['GET', 'POST'])
def update_post(postid):
    newcomments = request.form['comment']
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """UPDATE POSTS
                           SET COMMENTS =%s
                                WHERE (POST_ID = %s)"""
        cursor.execute(query, (newcomments, postid))
        connection.commit()
        flash("Your comment has been updated.")
        return redirect(url_for('page.profile_page'))

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

@page.route("/userprofiles/<user_id>")
def user_profiles(user_id):
    if current_user.get_id() is not None:
        if current_user.get_user_id()[0] == int(user_id):
            return redirect(url_for('page.profile_page'))
        else:
            with dbapi2._connect(app.config['dsn']) as connection:

                    cursor = connection.cursor()

                    query = "SELECT USERNAME FROM USERS WHERE (ID = %s)"

                    cursor.execute(query, (user_id,))

                    usr = cursor.fetchone()

                    user = User(usr[0],"","")

                    if user is not None:
                        movies = []
                        lists = []
                        userid = user_id
                        with dbapi2._connect(current_app.config['dsn']) as connection:
                            cursor = connection.cursor()
                            query = """SELECT TITLE, YEAR, m.SCORE, VOTES, IMDB_URL FROM MOVIES m
                                     INNER JOIN WATCHEDLIST w ON (m.MOVIEID = w.MOVIEID)
                                     WHERE (w.USERNAME = %s) """

                            cursor.execute(query, (user.username, ))

                        for movie in cursor:
                             movies.append(movie)

                        query = """SELECT DISTINCT LIST_NAME FROM MOVIELIST WHERE (USER_ID = %s)"""

                        cursor.execute(query, (userid, ))

                        for list in cursor:
                            lists.append(list[0])

                        followingusers = []
                        followingusers = user.get_following_users_by_userid()

                        followedusers = []
                        followedusers = user.get_followed_users_by_userid()

                        posts = []
                        posts = user.get_posts()
                        connection.commit()

                        currentuserid = current_user.get_user_id()
                        return render_template('userprofiles.html',userid=user_id, username=user.username, lists = lists, movies = movies, posts = posts, followingusers = followingusers, currentuserid = currentuserid,
                                                                    followedusers = followedusers)
                    else:
                        flash("There is no such user.")
                        return redirect(url_for('page.home_page'))

    else:
        flash("Please log in to MovieShake")
        return redirect(url_for('page.login_page'))

@page.route("/searchresults", methods = ['GET', 'POST'])
def search_users():

    if current_user.get_id() is None:
        flash("Please log in to MovieShake.")
        return redirect(url_for('page.login_page'))
    else:
        username_to_search = request.form['search_uname']
        with dbapi2._connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT ID FROM USERS WHERE (USERNAME = %s)"
            cursor.execute(query, (username_to_search,))
            userid = cursor.fetchone()
        if userid is not None:
            return redirect(url_for('page.user_profiles', user_id = userid[0]))
        else:
            flash("We could not find " + username_to_search + ". He/She might be missing :)")
            return redirect(url_for('page.home_page'))

@page.route("/list", methods = ['GET', 'POST'])
def list_page():
    if request.method == "POST":

        flag = False

        if current_user.username is None:
            flash('Please log in.')
            return redirect(url_for('page.login_page'))

        else:

            list_name = request.form['name']
            movie1 = request.form['moviename1']
            movie2 = request.form['moviename2']
            movie3 = request.form['moviename3']
            movie4 = request.form['moviename4']

            list_array = [movie1.title(),movie2.title(),movie3.title(),movie4.title()]

            smovie = Movie(list_array[0], "", "", "", "" )
            movie = smovie.search_movie_in_db()
            newlist = MovieList(current_user.get_user_id(),movie, list_name)


            for movie in list_array:
                if movie == "":
                    continue
                else:
                    smovie = Movie(movie, "", "", "", "" )
                    movie = smovie.search_movie_in_db()

                    if movie == -1:
                        movieToAdd = smovie.verify_movie_from_api()
                        if (movieToAdd == -1):
                            flash("There is no such movie")
                            return redirect(url_for('page.home_page'))
                        else:
                            movieToAdd.score = 7

                            movieToAdd.add_movie_to_db()
                            movieid = movieToAdd.search_movie_in_db()
                            newlist = MovieList(current_user.get_user_id(),movieid[0], list_name)
                            newlist.add_movie()

                    else:
                        newlist = MovieList(current_user.get_user_id(),movie, list_name)
                        if newlist.exists() == 1:
                            flash('You have already added that movie.')
                            return redirect(url_for('page.list_page'))
                        else:
                            newlist.add_movie()


            return redirect(url_for('page.home_page'))

    else:
        return render_template('list.html')

@page.route("/showlist/<listname>")
def Show_list(listname):
    movies = []
    listnames = []
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT MOVIEID, TITLE, YEAR, SCORE, VOTES, IMDB_URL FROM MOVIES m
                                 INNER JOIN MOVIELIST l ON (m.MOVIEID = l.MOVIE_ID)
                                 WHERE ((l.LIST_NAME = %s) AND (l.USER_ID = %s))"""

        user_id = current_user.get_user_id()
        cursor.execute(query, (listname,user_id,))

        for movie in cursor:
            movies.append(movie)

        connection.commit()
        listnames.append(listname)
    return render_template('movielist.html', movies = movies, listname = listnames)

@page.route("/userprofiles/showotherslist/<userid>/<listname>")
def Show_others_list(userid, listname):
    movies = []
    listnames = []
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT MOVIEID, TITLE, YEAR, SCORE, VOTES, IMDB_URL FROM MOVIES m
                                 INNER JOIN MOVIELIST l ON (m.MOVIEID = l.MOVIE_ID)
                                 WHERE ((l.LIST_NAME = %s) AND (l.USER_ID = %s))"""

        cursor.execute(query, (listname,userid,))

        for movie in cursor:
            movies.append(movie)

        connection.commit()
        listnames.append(listname)
    return render_template('movielistforeign.html', movies = movies, listname = listnames, userid = userid)

@page.route("/deletelist/<listname>")
def DeleteWholeList(listname):

    userid = current_user.get_user_id()
    listToDelete = MovieList(userid, "", listname)

    listToDelete.delete_list()
    flash(listname + " successfully deleted.")
    return redirect(url_for('page.profile_page'))

@page.route("/removefromlist/<listname>/<movieid>")
def RemoveMovieFromList(listname, movieid):
    userid = current_user.get_user_id()
    listToDelete = MovieList(userid, movieid, listname)

    listToDelete.removeMovieFromList()
    flash("Selected movie successfully removed from "+listname+".")
    return redirect(url_for('page.profile_page'))

@page.route("/oscars", methods= ['GET', 'POST'])
def oscars():
    winners = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM OSCARS"""

        cursor.execute(query)

        for winner in cursor:
            winners.append(winner)

        connection.commit()

    return render_template('oscars.html', winners = winners)

@page.route("/oscarsreverseorder", methods= ['GET', 'POST'])
def oscarsreverseorder():
    winnersreverse = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM OSCARS ORDER BY YEAR"""

        cursor.execute(query)

        for winner in cursor:
            winnersreverse.append(winner)

        connection.commit()

    return render_template('oscarsreverseorder.html', winnersreverse = winnersreverse)

@page.route("/oscaractor", methods= ['GET', 'POST'])
def oscaractor():
    persons = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
         cursor = connection.cursor()
         query = """SELECT NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY, YEAR FROM ACTORS a INNER JOIN OSCARS o
                             ON (((a.NAME = o.ACTRESS_NAME) AND (a.SURNAME = o.ACTRESS_SURNAME)) OR
                             ((a.NAME = o.ACTOR_NAME) AND (a.SURNAME = o.ACTOR_SURNAME)))
                             WHERE (((a.NAME = o.ACTRESS_NAME) AND (a.SURNAME = o.ACTRESS_SURNAME)) OR
                             ((a.NAME = o.ACTOR_NAME) AND (a.SURNAME = o.ACTOR_SURNAME)))
                             ORDER BY YEAR DESC"""
         cursor.execute(query)

         for person in cursor:
            persons.append(person)

         connection.commit()

    return render_template('oscaractor.html', persons = persons)

@page.route("/nominees", methods= ['GET', 'POST'])
def nominees():
    candidates = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM NOMINEES ORDER BY ID"""

        cursor.execute(query)

        for candidate in cursor:
            candidates.append(candidate)

        connection.commit()

    return render_template('nominees.html', candidates = candidates)


@page.route("/nominee_vote/<nominee_ID>", methods= ['GET', 'POST'])
def nominee_vote(nominee_ID):
    candidates = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """UPDATE NOMINEES SET VOTES = VOTES+1 WHERE ID = '""" + nominee_ID + """'"""
        cursor.execute(query)

        query = """SELECT * FROM NOMINEES ORDER BY VOTES DESC"""
        cursor.execute(query)

        for candidate in cursor:
            candidates.append(candidate)

        connection.commit()

    return render_template('nominee_vote.html', candidates = candidates)

@page.route('/series', methods = ['GET', 'POST'])
def series():

    nums = []
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM SERIES"""

        cursor.execute(query)

        for num in cursor:
            nums.append(num)

        connection.commit()
    return render_template('series.html', nums = nums)



@page.route("/series/<id>", methods= ['GET', 'POST'])
def series_comments(id):
    comments = []

    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM COMMENTS WHERE COMMENTS.SERIE_ID=2 """
        cursor.execute(query)

        for comment in cursor:
            comments.append(comment)

        connection.commit()
    return render_template('comments.html', comments = comments)

@page.route('/news', methods = ['GET', 'POST'])
def news():

    nums = []
    with dbapi2._connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM NEWS"""

        cursor.execute(query)

        for num in cursor:
            nums.append(num)

        connection.commit()
    return render_template('news.html', nums = nums)

@page.route('/deletefromwatched/<username>/<movieid>')
def DeleteFromWatchedList(username, movieid):
    movieToDelete = WatchedList(username, movieid, "")
    score = movieToDelete.existsInWatchedList()
    
    movieToDelete = WatchedList(username, movieid, score)
    
    movieToDelete.delete_from_watched_list()
    
    movie = Movie("","","","","")
    oldvotes = movie.getvotes_in_movie_db(movieid)
    oldscore = movie.getscore_in_movie_db(movieid)
    
    if int(oldvotes[0]) > 1:
        total = int(oldvotes)*int(oldscore)
        total = total - score
        newvotes = oldvotes - 1
        newscore = total / newvotes
        movie.update_votes_and_score(movieid, newscore, newvotes)
    
    return redirect(url_for('page.home_page'))


                


