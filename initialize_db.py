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
                        'BLANCHETT',
                        'MATTHEW',
                        'McCONAUGHEY',
                        '2013')""")

    cursor.execute("""INSERT INTO OSCARS (MOVIE, ACTRESS_NAME, ACTRESS_SURNAME, ACTOR_NAME, ACTOR_SURNAME, YEAR) VALUES(
                        'ARGO',
                        'JENNIFER',
                        'LAWRENCE',
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

    # Nominees table
    cursor.execute("""DROP TABLE IF EXISTS NOMINEES CASCADE""")
    cursor.execute("""CREATE TABLE NOMINEES(
                        ID SERIAL PRIMARY KEY NOT NULL,
                        NAME VARCHAR(50) NOT NULL,
                        INFORMATION VARCHAR(300),
                        PICTUREURL VARCHAR(200),
                        DIRECTOR VARCHAR(40),
                        VOTES INTEGER)""")

    # Data for nominee table
    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'CALL ME BY YOUR NAME',
                    'In Northern Italy in 1983, seventeen year-old Elio begins a relationship with visiting Oliver, his father''s research assistant, with whom he bonds over his emerging sexuality, their Jewish heritage, and the beguiling Italian landscape.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BNDk3NTEwNjc0MV5BMl5BanBnXkFtZTgwNzYxNTMwMzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'LUCA GUADAGNINO',
                    '14')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'LADY BIRD',
                    'In the early 2000s, an artistically-inclined seventeen year-old comes of age in Sacramento, California.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjg1NDY0NDYzMV5BMl5BanBnXkFtZTgwNzIwMTEwNDI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'GRETA GERWIG',
                    '12')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'MOLLY''S GAME',
                  'The true story of Molly Bloom, an Olympic-class skier who ran the world''s most exclusive high-stakes poker game and became an FBI target.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMzM3NzcxMzQyNl5BMl5BanBnXkFtZTgwNzUyNzcxNDM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'AARON SORKIN',
                  '7')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'I, TONYA',
                    'Competitive ice skater Tonya Harding rises amongst the ranks at the U.S. Figure Skating Championships, but her future in the activity is thrown into doubt when her ex-husband intervenes.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjI5MDY1NjYzMl5BMl5BanBnXkFtZTgwNjIzNDAxNDM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'CRAIG GILLESPIE',
                    '7')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'DUNKIRK',
                  'Allied soldiers from Belgium, the British Empire and France are surrounded by the German Army, and evacuated during a fierce battle in World War II.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BN2YyZjQ0NTEtNzU5MS00NGZkLTg0MTEtYzJmMWY3MWRhZjM2XkEyXkFqcGdeQXVyMDA4NzMyOA@@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'CHRISTOPHER NOLAN',
                  '18')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'BATTLE OF THE SEXES',
                    'The true story of the 1973 tennis match between World number one Billie Jean King and ex-champ and serial hustler Bobby Riggs.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BZTljYmU2NTMtODhhNC00NjlhLWJhZTUtNDllODYyYWM4ZjA5XkEyXkFqcGdeQXVyNjM0ODk5NDY@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'JONATHAN DAYTON, VALERIE FARIS',
                    '22')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'MUDBOUND',
                  'Two men return home from World War II to work on a farm in rural Mississippi, where they struggle to deal with racism and adjusting to life after war.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BZTg3YTEzNjYtZTY2NS00YjNmLTlhNjUtZTI2M2E5NDI4M2NjXkEyXkFqcGdeQXVyMzI3MDEzMzM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'DEE REES',
                  '12')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'THREE BILBOARDS OUTSIDE EBBING, MISSOURI',
                    'A mother personally challenges the local authorities to solve her daughter''s murder when they fail to catch the culprit.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjMxNzgwMDUyMl5BMl5BanBnXkFtZTgwMTQ0NTIyNDM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'MARTIN McDONAGH',
                    '9')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'THE SHAPE OF WATER',
                  'In a 1960s research facility, a mute janitor forms a relationship with an aquatic creature.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMTgwNzk3MTQ3Nl5BMl5BanBnXkFtZTgwODEwMDIzNDM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'GUILLERMO DEL TORO',
                  '9')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'MOTHER!',
                    'A couple''s relationship is tested when uninvited guests arrive at their home, disrupting their tranquil existence.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMzc5ODExODE0MV5BMl5BanBnXkFtZTgwNDkzNDUxMzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'DARREN ARONOFSKY',
                    '8')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'GET OUT',
                  'It''s time for a young African American to meet with his white girlfriend''s parents for a weekend in their secluded estate in the woods, but before long, the friendly and polite ambience will give way to a nightmare.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'JORDAN PEELE',
                  '10')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'WONDER WOMAN',
                    'When a pilot crashes and tells of conflict in the outside world, Diana, an Amazonian warrior in training, leaves home to fight a war, discovering her full powers and true destiny.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BNDFmZjgyMTEtYTk5MC00NmY0LWJhZjktOWY2MzI5YjkzODNlXkEyXkFqcGdeQXVyMDA4NzMyOA@@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'PATTY JENKINS',
                    '12')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'THE BIG SICK',
                  'Pakistan-born comedian Kumail Nanjiani and grad student Emily Gardner fall in love but struggle as their cultures clash. When Emily contracts a mysterious illness, Kumail finds himself forced to face her feisty parents, his family''s expectations, and his true feelings.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BZWM4YzZjOTEtZmU5ZS00ZTRkLWFiNjAtZTEwNzIzMDM5MjdmXkEyXkFqcGdeQXVyNDg2MjUxNjM@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'MICHEAL SHOWALTER',
                  '2')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'THE FLORIDA PROJECT',
                    'Set over one summer, the film follows precocious 6-year-old Moonee as she courts mischief and adventure with her ragtag playmates and bonds with her rebellious but caring mother, all while living in the shadows of Disney World.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjg4ZmY1MmItMjFjOS00ZTg2LWJjNDYtNDM2YmM2NzhiNmZhXkEyXkFqcGdeQXVyNTAzMTY4MDA@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'SEAN BAKER',
                    '18')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'DARKEST HOUR',
                  'During the early days of World War II, the fate of Western Europe hangs on the newly-appointed British Prime Minister Winston Churchill, who must decide whether to negotiate with Hitler, or fight on against incredible odds.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMjIyNDkyMTgzMV5BMl5BanBnXkFtZTgwNTQwNjg2MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'JOE WRIGHT',
                  '6')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'WONDERSTRUCK',
                    'The story of a young boy in the Midwest is told simultaneously with a tale about a young girl in New York from fifty years ago as they both seek the same mysterious connection.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjM3NjY0MTYwM15BMl5BanBnXkFtZTgwMDI5NzA2MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'TODD HAYNES',
                    '7')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'BLADE RUNNER 2049',
                  'A young blade runner''s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who''s been missing for thirty years.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'DENIS VILLENEUVE',
                  '3')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'THE DISASTER ARTIST',
                    'When Greg Sestero, an aspiring film actor, meets the weird and mysterious Tommy Wiseau in an acting class, they form a unique friendship and travel to Hollywood to make their dreams come true.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BOGNkMzliMGMtMDI5Ni00OTZkLTgyMTYtNzk5ZTY1NjVhYjVmXkEyXkFqcGdeQXVyNTAzMTY4MDA@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'JAMES FRANCO',
                    '5')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'STRONGER',
                    'Stronger is the inspiring real life story of Jeff Bauman, an ordinary man who captured the hearts of his city and the world to become a symbol of hope after surviving the 2013 Boston Marathon bombing.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjE0NjIwMjQ2MF5BMl5BanBnXkFtZTgwNTAxMzQ5MjI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'DAVID GORDON GREEN',
                    '9')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'DETROIT',
                  'Fact-based drama set during the 1967 Detroit riots in which a group of rogue police officers respond to a complaint with retribution rather than justice on their minds.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMTg4MDk4MTUxMF5BMl5BanBnXkFtZTgwNDE5NjA5MjI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'KATHRYN BIGELOW',
                  '11')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'THE KILLING OF A SACRED DEER',
                    'Steven, a charismatic surgeon, is forced to make an unthinkable sacrifice after his life starts to fall apart, when the behavior of a teenage boy he has taken under his wing turns sinister.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjU4NDcwOTA2NF5BMl5BanBnXkFtZTgwMjE2OTg4MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'YORGOS LANTHIMOS',
                    '6')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'BREATHE',
                  'The inspiring true love story of Robin and Diana Cavendish, an adventurous couple who refuse to give up in the face of a devastating disease. Their heartwarming celebration of human possibility marks the directorial debut of Andy Serkis.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMTg1OTcxNjU1MV5BMl5BanBnXkFtZTgwMzcwMTQ3MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'ANDY SERKIS',
                  '8')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                    'LAST FLAG FLYING',
                    'Thirty years after they served together in Vietnam, a former Navy Corpsman Larry "Doc" Shepherd re-unites with his old buddies, former Marines Sal Nealon and Reverend Richard Mueller, to bury his son, a young Marine killed in the Iraq War.',
                    'https://images-na.ssl-images-amazon.com/images/M/MV5BMjI3MDAxNTg1OF5BMl5BanBnXkFtZTgwMzMzMDM1MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
                    'RICHARD LINKLATER',
                    '4')""")

    cursor.execute("""INSERT INTO NOMINEES (NAME, INFORMATION, PICTUREURL, DIRECTOR, VOTES) VALUES(
                  'WONDER WHEEL',
                  'On Coney Island in the 1950s, a lifeguard tells the story of a middle-aged carousel operator and his beleaguered wife.',
                  'https://images-na.ssl-images-amazon.com/images/M/MV5BMTA2NjAyMDIzMzleQTJeQWpwZ15BbWU4MDg1NTEwNjMy._V1_UX182_CR0,0,182,268_AL_.jpg',
                  'WOODY ALLEN',
                  '2')""")







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


    cursor.execute("""INSERT INTO SERIES (TITLE, STARTYEAR, ENDYEAR, SCORE, VOTES,PICTURE,DESCRIPTION) VALUES(
                  'Game Of Thrones',
                  '2011',
                  '2018',
                  '9.6',
                  '1442',
                  'http://cdn.pastemagazine.com/www/blogs/lists/winter-is-coming-game-of-thrones.jpg',
                  'Nine noble families fight for control over the mythical lands of Westeros, while a forgotten race returns after being dormant for thousands of years.'
                    )""")

    # News table
    cursor.execute("""DROP TABLE IF EXISTS NEWS CASCADE""")
    cursor.execute("""CREATE TABLE NEWS(
                                    ID SERIAL PRIMARY KEY NOT NULL,
                                    TITLE VARCHAR(100),
                                    PICTURE VARCHAR(500),
                                    DESCRIPTION VARCHAR(1000) )""")


        # Comments table
    cursor.execute("""DROP TABLE IF EXISTS COMMENTS CASCADE""")
    cursor.execute("""CREATE TABLE COMMENTS (
                                    ID SERIAL PRIMARY KEY NOT NULL,
                                    USER_NAME VARCHAR(100),
                                    SERIE_ID INT NOT NULL,
                                    DESCRIPTION VARCHAR(1000),
                                        FOREIGN KEY (USER_NAME) REFERENCES USERS(USERNAME) ON DELETE CASCADE ON UPDATE CASCADE,
                                        FOREIGN KEY (SERIE_ID) REFERENCES SERIES(ID) ON DELETE CASCADE ON UPDATE CASCADE )""")
    cursor.execute("""INSERT INTO COMMENTS (USER_NAME, SERIE_ID, DESCRIPTION) VALUES(
                  'tugrul',
                  '1',
                  'Nine noble families fight for control over the mythical lands of Westeros, while a forgotten race returns after being dormant for thousands of years.'
                    )""")




