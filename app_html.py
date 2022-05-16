from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_harwoodt'
app.config['MYSQL_PASSWORD'] = '7358' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_harwoodt'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Data

movies_from_app_py = [
{
    "movieName": "Django Unchained",
    "releaseYear": 2012,
    "rating": 8.4,
    "movieLength": 165,
    "genreName": "Western",
    "actorName": "Jamie Foxx, Leonardo DiCaprio",
    "directorName": "Quentin Tarantino"
},
{
    "movieName": "Anchorman: The Legend of Ron Burgundy",
    "releaseYear": 2004,
    "rating": 7.1,
    "movieLength": 94,
    "genreName": "Comedy",
    "actorName": "Will Ferrell, Steve Carell",
    "directorName": "Adam McKay"
},
{
    "movieName": "Don't Look Up",
    "releaseYear": 2021,
    "rating": 7.2,
    "movieLength": 138,
    "genreName": "Comedy",
    "actorName": "Jennifer Lawrence, Leonardo DiCaprio",
    "directorName": "Adam McKay"
},
{
    "movieName": "Kill Bill: Vol. 1",
    "releaseYear": 2003,
    "rating": 8.2,
    "movieLength": 111,
    "genreName": "Action",
    "actorName": "Uma Thurman, David Carradine",
    "directorName": "Quentin Tarantino"
},
{
    "movieName": "John Wick",
    "releaseYear": 2014,
    "rating": 7.4,
    "movieLength": 101,
    "genreName": "Action",
    "actorName": "Keanu Reeves, Michael Nyqvist",
    "directorName": "Chad Stahelski"
},
]

actors_from_app_py = [
{
    "idActor": 1,
    "actorName": "Jamie Foxx",
    "age": 54
},
{
    "idActor": 2,
    "actorName": "Leonardo DiCaprio",
    "age": 47
},
{
    "idActor": 3,
    "actorName": "Will Ferrell",
    "age": 54
},
{
    "idActor": 4,
    "actorName": "Steve Carell",
    "age": 59
},
{
    "idActor": 5,
    "actorName": "Jennifer Lawrence",
    "age": 31
},
{
    "idActor": 6,
    "actorName": "Uma Thurman",
    "age": 51
},
{
    "idActor": 7,
    "actorName": "David Carradine",
    "age": 72
},
{
    "idActor": 8,
    "actorName": "Keanu Reeves",
    "age": 57
},
{
    "idActor": 9,
    "actorName": "Michael Nyqvist",
    "age": 56
},
]

movie_actors_from_app_py = [
{
    "idMovie": 1,
    "movieName": "Django Unchained",
    "idActor": 1,
    "actorName": "Jamie Foxx"
},
{
    "idMovie": 1,
    "movieName": "Django Unchained",
    "idActor": 2,
    "actorName": "Leonardo DiCaprio"
},
{
    "idMovie": 2,
    "movieName": "Anchorman: The Legend of Ron Burgundy",
    "idActor": 3,
    "actorName": "Will Ferrell"
},
{
    "idMovie": 2,
    "movieName": "Anchorman: The Legend of Ron Burgundy",
    "idActor": 4,
    "actorName": "Steve Carell"
},
{
    "idMovie": 3,
    "movieName": "Don't Look Up",
    "idActor": 2,
    "actorName": "Leonardo DiCaprio"
},
{
    "idMovie": 3,
    "movieName": "Don't Look Up",
    "idActor": 5,
    "actorName": "Jennifer Lawrence"
},
{
    "idMovie": 4,
    "movieName": "Kill Bill: Vol. 1",
    "idActor": 6,
    "actorName": "Uma Thurman"
},
{
    "idMovie": 4,
    "movieName": "Kill Bill: Vol. 1",
    "idActor": 7,
    "actorName": "David Carradine"
},
{
    "idMovie": 5,
    "movieName": "John Wick",
    "idActor": 8,
    "actorName": "Keanu Reeves"
},
{
    "idMovie": 5,
    "movieName": "John Wick",
    "idActor": 9,
    "actorName": "Michael Nyqvist"
},
]

genre_actors_from_app_py = [
{
    "idGenre": 1,
    "genreName": "Western",
    "idActor": 1,
    "actorName": "Jamie Foxx"
},
{
    "idGenre": 1,
    "genreName": "Western",
    "idActor": 2,
    "actorName": "Leonardo DiCaprio"
},
{
    "idGenre": 2,
    "genreName": "Comedy",
    "idActor": 3,
    "actorName": "Will Ferrell"
},
{
    "idGenre": 2,
    "genreName": "Comedy",
    "idActor": 4,
    "actorName": "Steve Carell"
},
{
    "idGenre": 2,
    "genreName": "Comedy",
    "idActor": 2,
    "actorName": "Leonardo DiCaprio"
},
{
    "idGenre": 2,
    "genreName": "Comedy",
    "idActor": 5,
    "actorName": "Jennifer Lawrence"
},
{
    "idGenre": 3,
    "genreName": "Action",
    "idActor": 6,
    "actorName": "Uma Thurman"
},
{
    "idGenre": 3,
    "genreName": "Action",
    "idActor": 7,
    "actorName": "David Carradine"
},
{
    "idGenre": 3,
    "genreName": "Action",
    "idActor": 8,
    "actorName": "Keanu Reeves"
},
{
    "idGenre": 3,
    "genreName": "Action",
    "idActor": 9,
    "actorName": "Michael Nyqvist"
},
]

genre_directors_from_app_py = [
{
    "idDirector": 1,
    "directorName": "Quentin Tarantino",
    "idGenre": 1,
    "genreName": "Western",
},
{
    "idDirector": 2,
    "directorName": "Adam McKay",
    "idGenre": 2,
    "genreName": "Comedy",
},
{
    "idDirector": 1,
    "directorName": "Quentin Tarantino",
    "idGenre": 3,
    "genreName": "Action",
},
{
    "idDirector": 3,
    "directorName": "Chad Stahelski",
    "idGenre": 3,
    "genreName": "Action",
},
]

genres_from_app_py = [
{
    "idGenre": 1,
    "genreName": "Western"
},
{
    "idGenre": 2,
    "genreName": "Comedy"
},
{
    "idGenre": 3,
    "genreName": "Action"
},
]

directors_from_app_py = [
{
    "idDirector": 1,
    "directorName": "Quentin Tarantino",
    "age": 59
},
{
    "idDirector": 2,
    "directorName": "Adam McKay",
    "age": 54
},
{
    "idDirector": 3,
    "directorName": "Chad Stahelski",
    "age": 53
},
]


# Routes

@app.route('/')
def root():
    query1 = "SELECT * FROM Actors;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()

    return results[0]

@app.route('/movies')
def root():
    return render_template("movies.j2", movies=movies_from_app_py)

@app.route('/movie_actors')
def movie_actors():
    return render_template("movie_actors.j2", movie_actors=movie_actors_from_app_py)

@app.route('/genre_actors')
def genre_actors():
    return render_template("genre_actors.j2", genre_actors=genre_actors_from_app_py)

@app.route('/genre_directors')
def genre_directors():
    return render_template("genre_directors.j2", genre_directors=genre_directors_from_app_py)

@app.route('/actors')
def actors():
    return render_template("actors.j2", actors=actors_from_app_py)

@app.route('/directors')
def directors():
    return render_template("directors.j2", directors=directors_from_app_py)

@app.route('/genres')
def genres():
    return render_template("genres.j2", genres=genres_from_app_py)


# Listener

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 9987))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=9987, debug=True)