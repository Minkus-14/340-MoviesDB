from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

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
    return render_template("main.j2", movies=movies_from_app_py)

# @app.route('/movies')
# def movies():
#     return render_template("movies.j2", movies=movies_from_app_py)

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
    port = int(os.environ.get('PORT', 9987))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)