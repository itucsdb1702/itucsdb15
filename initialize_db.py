def initialize_db_function(cursor):


    # Actors table
    cursor.execute("""DROP TABLE IF EXISTS ACTORS CASCADE""")
    cursor.execute("""CREATE TABLE ACTORS(
                        ID SERIAL PRIMARY KEY NOT NULL,
                        NAME VARCHAR(30),
                        SURNAME VARCHAR(30),
                        GENDER VARCHAR(6),
                        BIRTHDATE VARCHAR(15),
                        COUNTRY VARCHAR(15))""")

    # Data for Actor table
    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'ANGELINA',
                    'JOLIE',
                    'FEMALE',
                    '1975-6-4',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'NATALIE',
                    'PORTMAN',
                    'FEMALE',
                    '1981-6-9',
                    'ISRAEL')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'JULIA',
                    'ROBERTS',
                    'FEMALE',
                    '1967-10-28',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'ANTHONY',
                    'HOPKINS',
                    'MALE',
                    '1937-12-31',
                    'UK')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'BRIE',
                    'LARSON',
                    'FEMALE',
                    '1989-10-1',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'JULIANNE',
                    'MOORE',
                    'FEMALE',
                    '1960-12-3',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'CASEY',
                    'AFFLECK',
                    'MALE',
                    '1975-8-12',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'LEONARDO',
                    'DICAPRIO',
                    'MALE',
                    '1974-11-11',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'EDDIE',
                    'REDMAYNE',
                    'MALE',
                    '1982-1-6',
                    'UK')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'MATTHEW',
                    'McCONAUGHEY',
                    'MALE',
                    '1969-11-4',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'EVA',
                    'GREEN',
                    'FEMALE',
                    '1980-7-6',
                    'FRANCE')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'CATE',
                    'BLANCHETT',
                    'FEMALE',
                    '1969-5-14',
                    'AUSTRALIA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'DANIEL',
                    'DAY-LEWIS',
                    'MALE',
                    '1957-4-29',
                    'UK')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'JEAN',
                    'DUJARDIN',
                    'MALE',
                    '1972-6-19',
                    'FRANCE')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'COLIN',
                    'FIRTH',
                    'MALE',
                    '1960-9-10',
                    'UK')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'EMMA',
                    'STONE',
                    'FEMALE',
                    '1988-11-6',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'JENNIFER',
                    'LAWRENCE',
                    'FEMALE',
                    '1990-8-15',
                    'USA')""")

    cursor.execute("""INSERT INTO ACTORS (NAME, SURNAME, GENDER, BIRTHDATE, COUNTRY) VALUES(
                    'MERYL',
                    'STREEP',
                    'FEMALE',
                    '1949-6-22',
                    'USA')""")

    # Oscars table
    cursor.execute("""DROP TABLE IF EXISTS OSCARS CASCADE""")
    cursor.execute("""CREATE TABLE OSCARS(
                    MOVIE VARCHAR(30),
                    ACTRESS_NAME VARCHAR(30),
                    ACTRESS_SURNAME VARCHAR(30),
                    ACTOR_NAME VARCHAR(30),
                    ACTOR_SURNAME VARCHAR(30),
                    YEAR INT PRIMARY KEY NOT NULL)""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'MOONLIGHT',
                        'EMMA',
                        'STONE',
                        'CASEY',
                        'AFFLECK',
                        '2016')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'SPOTLIGHT',
                        'BRIE',
                        'LARSON',
                        'LEONARDO',
                        'DICAPRIO',
                        '2015')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'BIRDMAN',
                        'JULIANNE',
                        'MOORE',
                        'EDDIE',
                        'REDMAYNE',
                        '2014')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        '12 YEARS A SLAVE',
                        'CATE',
                        'LANCHETT',
                        'MATTHEW',
                        'McCONAUGHEY',
                        '2013')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'ARGO',
                        'JENNIFER',
                        'LAWRANCE',
                        'DANIEL',
                        'DAY-LEWIS',
                        '2012')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'THE ARTIST',
                        'MERYL',
                        'STREEP',
                        'JEAN',
                        'DUJARDIN',
                        '2011')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'THE KING''S SPEECH',
                        'NATALIE',
                        'PORTMAN',
                        'COLIN',
                        'FIRTH',
                        '2010')""")



     # Series table
    cursor.execute("""DROP TABLE IF EXISTS SERIES CASCADE""")
    cursor.execute("""CREATE TABLE SERIES(
                                    ID SERIAL PRIMARY KEY NOT NULL,
                                    TITLE VARCHAR(100),
                                    STARTYEAR INTEGER,
                                    ENDYEAR INTEGER,
                                    SCORE FLOAT,
                                    VOTES INTEGER,
                                    PICTURE VARCHAR(500),
                                    DESCRIPTION VARCHAR(1000) )""")

    cursor.execute("""INSERT INTO SERIES (TITLE, STARTYEAR, ENDYEAR, SCORE,VOTES, PICTURE, DESCRIPTION) VALUES(
                    'Game Of Thrones',
                    '2011',
                    '2018',
                    '9.6',
                    '1424',
                    'http://cdn.pastemagazine.com/www/blogs/lists/winter-is-coming-game-of-thrones.jpg',
                    'Nine noble families fight for control over the mythical lands of Westeros, while a forgotten race returns after being dormant for thousands of years.')""")

    cursor.execute("""INSERT INTO SERIES (TITLE, STARTYEAR, ENDYEAR, SCORE, VOTES,PICTURE, DESCRIPTION) VALUES(
                    'Game Of ',
                    '2011',
                    '2018',
                    '9.6',
                    '1424',
                    'http://cdn.pastemagazine.com/www/blogs/lists/winter-is-coming-game-of-thrones.jpg',
                    'Nine noble families fight for control over the mythical lands of Westeros, while a forgotten race returns after being dormant for thousands of years.')""")
