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
                    'EVA',
                    'GREEN',
                    'FEMALE',
                    '1980-7-6',
                    'FRANCE')""")



