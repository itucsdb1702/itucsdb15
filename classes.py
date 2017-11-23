import psycopg2 as dbapi2
from flask import current_app as app
from flask_login import UserMixin
from flask import flash
from flask_login import login_manager, login_user, logout_user
from passlib.apps import custom_app_context as pwd_context
from flask_login.login_manager import LoginManager
import requests

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
            
class Movie:
    def __init__(self, title, year, score, votes, imdb_url):
        self.title = title
        self.year = year
        self.score = score
        self.votes = votes
        self.imdb_url = imdb_url
        
    def search_movie_in_db(self):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT MOVIEID FROM MOVIES WHERE (TITLE = %s)"
            cursor.execute(query, (self.title, ))
            movie = cursor.fetchone()

            if movie is not None:
                return movie
            else:
                return -1
    
    def getscore_in_movie_db(self, movieid):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT SCORE FROM MOVIES WHERE (MOVIEID = %s)"
            cursor.execute(query, (movieid, ))
            movie = cursor.fetchone()

            if movie is not None:
                return movie
            else:
                return -1
    
    def getvotes_in_movie_db(self, movieid):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT VOTES FROM MOVIES WHERE (MOVIEID = %s)"
            cursor.execute(query, (movieid, ))
            movie = cursor.fetchone()

            if movie is not None:
                return movie
            else:
                return -1
    
    def verify_movie_from_api(self):
        
        title = self.title.replace(' ', '+')
        url = "http://www.omdbapi.com/?apikey=e5ccb3ca&t="+ self.title
        response = requests.get(url).json()
    
        if(response['Response'] == "False"):
            return -1
        
        else:
            title = response['Title']
            year = response['Year']
            votes = 1
            imdb_url = "http://www.imdb.com/title/" + response['imdbID']
            
            movie = Movie(title, year, "", votes, imdb_url)
            
            return movie
        
    def add_movie_to_db(self):
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO MOVIES (TITLE, YEAR, SCORE, VOTES, IMDB_URL) 
                    VALUES (%s, %s, %s, %s, %s)"""
    
                    cursor.execute(query, (self.title, self.year, self.score, self.votes, self.imdb_url))
                    connection.commit()
                    
    def update_votes_and_score(self, movieid, score, votes):
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """UPDATE MOVIES
                            SET SCORE = %s, VOTES= %s
                            WHERE MOVIEID = %s;"""
    
                    cursor.execute(query, (score, votes, movieid))
                    connection.commit()
        
        
        
class WatchedList:
    def __init__(self, username, movieid, score):          
        self.username = username
        self.movieid = movieid
        self.score = score
    
    def add_movie_user_pair(self):
            with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO WATCHEDLIST (USERNAME, MOVIEID, SCORE) 
                    VALUES (%s, %s, %s)"""
    
                    cursor.execute(query, (self.username, self.movieid, self.score))
                    connection.commit()
    def existsInWatchedList(self):
         with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """SELECT MOVIEID FROM WATCHEDLIST WHERE ((USERNAME = %s) AND (MOVIEID = %s)) """
    
                    cursor.execute(query, (self.username, self.movieid))
                    id = cursor.fetchone()
                    
                    if id is None:
                        return False
                    else:
                        return True
    


    