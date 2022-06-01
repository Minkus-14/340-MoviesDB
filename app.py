# Group 99: The Gretzky Coalition
# Code adapted from https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, redirect
import database.db_connector as db
from flask import request
import os
from flask_mysqldb import MySQL

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

db_connection.ping(True)

# Routes

@app.route('/')
def root():
    return redirect("/movies")

@app.route('/movies', methods=["POST", "GET"])
def movies():
    # Separate out the request methods, in this case this is for a POST
    # insert a movie into the Movies entity
    if request.method == "POST":
        # fire off if user presses the Add Movie button
        if request.form.get("Add_Movies"):
            # grab user form inputs
            movieName = request.form["movieName"]
            releaseYear = request.form["releaseYear"]
            rating = request.form["rating"]
            movieLength = request.form["movieLength"]
            idDirector = request.form["idDirector"]
            idGenre = request.form["idGenre"]

            # account for null rating, movieLength and idGenre
            if (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None"):
                # mySQL query to insert a new movie into Movie with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, idDirector) VALUES (%s, %s,%s)"
                
                db.execute_query(db_connection, query, (movieName, releaseYear, idDirector))

            # account for null movieLength and idGenre
            elif (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, rating, idDirector) VALUES (%s, %s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, idDirector))

            # account for null rating and movieLength
            elif (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, idDirector) VALUES (%s, %s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, idDirector))

            # account for null rating and idGenre
            elif (rating == "" or rating == "None") and (idGenre == "" or idGenre == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, movieLength, idDirector) VALUES (%s, %s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, movieLength, idDirector))

            # account for null rating
            elif rating == "" or rating == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, movieLength, idDirector) VALUES (%s, %s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, movieLength, idDirector))
                
            # account for null movieLength
            elif movieLength == "" or movieLength == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, rating, idDirector) VALUES (%s, %s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, idDirector))
                
            # account for null idGenre
            elif idGenre == "" or idGenre == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, rating, movieLength, idDirector) VALUES (%s, %s,%s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, movieLength, idDirector))
                
            # no null inputs
            else:
                query = "INSERT INTO Movies (movieName, releaseYear, rating, movieLength, idDirector, idGenre) VALUES (%s, %s,%s,%s,%s,%s)"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, movieLength, idDirector, idGenre))

            # redirect back to people page
            return redirect("/movies")

        if request.form.get("Search_Movies"):
            releaseYear = request.form["year"]
            # mySQL query to grab all the movies in Movies
            query1 = """SELECT Movies.idMovie AS 'ID', Movies.movieName AS 'Movie name', Movies.releaseYear AS 'Release Year',
                        Movies.rating AS 'Rating', Movies.movieLength AS 'Length (min)', Genres.genreName AS 'Genre', group_concat(Actors.actorName) AS 'Actors',
                        Directors.directorName AS 'Director Name' 
                        FROM Movies
                        LEFT JOIN Genres ON Movies.idGenre = Genres.idGenre
                        LEFT JOIN Directors ON Movies.idDirector = Directors.idDirector
                        LEFT JOIN Actors_has_Movies ON Movies.idMovie = Actors_has_Movies.idMovie
                        LEFT JOIN Actors ON Actors_has_Movies.idActor = Actors.idActor
                        WHERE releaseYear = %s
                        GROUP BY Movies.movieName
                        ORDER BY Movies.movieName ASC;"""
            data = db.execute_query(db_connection, query1, (releaseYear, )).fetchall()

            # mySQL query to grab director id/name data for our dropdown
            query2 = "SELECT idDirector, directorName FROM Directors"
            director_data = db.execute_query(db_connection, query2).fetchall()

            # mySQL query to grab genre id/name data for our dropdown
            query3 = "SELECT idGenre, genreName FROM Genres"
            genre_data = db.execute_query(db_connection, query3).fetchall()

            # mySQL query to year data for our dropdown
            query4 = """SELECT releaseYear FROM Movies
                        ORDER BY releaseYear ASC;"""
            year_data = db.execute_query(db_connection, query4).fetchall()

            # render movies page passing our query data
            return render_template("movies.j2", data=data, directors=director_data, genres=genre_data, years=year_data)

        if request.form.get("Show_All"):
            return redirect("/movies")

    # Grab movies data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the movies in Movies
        query1 = """SELECT Movies.idMovie AS 'ID', Movies.movieName AS 'Movie name', Movies.releaseYear AS 'Release Year',
        Movies.rating AS 'Rating', Movies.movieLength AS 'Length (min)', Genres.genreName AS 'Genre', group_concat(Actors.actorName) AS 'Actors',
        Directors.directorName AS 'Director Name' 
        FROM Movies
        LEFT JOIN Genres ON Movies.idGenre = Genres.idGenre
        LEFT JOIN Directors ON Movies.idDirector = Directors.idDirector
        LEFT JOIN Actors_has_Movies ON Movies.idMovie = Actors_has_Movies.idMovie
        LEFT JOIN Actors ON Actors_has_Movies.idActor = Actors.idActor
        GROUP BY Movies.movieName
        ORDER BY Movies.movieName ASC;"""
        
        data = db.execute_query(db_connection, query1).fetchall()

        # mySQL query to grab director id/name data for our dropdown
        query2 = "SELECT idDirector, directorName FROM Directors"
        director_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab genre id/name data for our dropdown
        query3 = "SELECT idGenre, genreName FROM Genres"
        genre_data = db.execute_query(db_connection, query3).fetchall()

        # mySQL query to year data for our dropdown
        query4 = """SELECT releaseYear FROM Movies
                    ORDER BY releaseYear ASC;"""
        year_data = db.execute_query(db_connection, query4).fetchall()

        # render movies page passing our query data
        return render_template("movies.j2", data=data, directors=director_data, genres=genre_data, years=year_data)

# route for edit functionality, updating the attributes of a movie in Movies
# similar to our delete route, we want to the pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/edit_movies/<int:id>", methods=["POST", "GET"])
def edit_movies(id):
    if request.method == "GET":
        # mySQL query to grab the info of the movie with our passed id
        query = "SELECT * FROM Movies WHERE idMovie = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to grab director id/name data for our dropdown
        query2 = "SELECT idDirector, directorName FROM Directors"
        director_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab genre id/name data for our dropdown
        query3 = "SELECT idGenre, genreName FROM Genres"
        genre_data = db.execute_query(db_connection, query3).fetchall()

        # render edit_movies page passing our query data to the edit_movies template
        return render_template("edit_movies.j2", data=data, directors=director_data, genres=genre_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Movies"):
            # grab user form inputs
            idMovie = request.form["idMovie"]
            movieName = request.form["movieName"]
            releaseYear = request.form["releaseYear"]
            rating = request.form["rating"]
            movieLength = request.form["movieLength"]
            idDirector = request.form["idDirector"]
            idGenre = request.form["idGenre"]

            # account for null rating, movieLength and idGenre
            if (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None") and (idGenre == "" or idGenre == "None"):
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, idDirector, idMovie))

            # account for null rating and idGenre
            elif (rating == "" or rating == "None") and (idGenre == "" or idGenre == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.movieLength = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, movieLength, idDirector, idMovie))

            # account for null movieLength and idGenre
            elif (idGenre == "" or idGenre == "None") and (movieLength == "" or movieLength == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, idDirector, idMovie))

            # account for null movieLength and rating
            elif (idGenre == "" or idGenre == "None") and (rating == "" or rating == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, idDirector, idGenre, idMovie))

            # account for null rating
            elif rating == "" or rating == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.movieLength = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, movieLength, idDirector, idGenre, idMovie))

            # account for null movieLength
            elif movieLength == "" or movieLength == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, idDirector, idGenre, idMovie))

            # account for null idGenre
            elif movieLength == "" or movieLength == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.movieLength = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, movieLength, idDirector, idMovie))

            # no null inputs
            else:
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.movieLength = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                db.execute_query(db_connection, query, (movieName, releaseYear, rating, movieLength, idDirector, idGenre, idMovie))

            # redirect back to Movies page after we execute the update query
            return redirect("/movies")

# route for delete functionality, deleting a movie from Movies,
# we want to pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/delete_movies/<int:id>")
def delete_movies(id):
    # mySQL query to delete the movie with our passed id
    query = "DELETE FROM Movies WHERE idMovie = '%s';"
    db.execute_query(db_connection, query, (id,))

    # redirect back to movie page
    return redirect("/movies")

# route for delete functionality, deleting a movie from Movies,
# we want to pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/search_movies", methods=["POST", "GET"])
def search_movies():
    # Separate out the request methods, in this case this is for a POST
    # insert a movie into the Movies entity
    if request.method == "POST":
        if request.form.get("Search_Movies"):
            releaseYear = request.form["year"]
            # mySQL query to grab all the movies in Movies
            query1 = """SELECT Movies.idMovie AS 'ID', Movies.movieName AS 'Movie name', Movies.releaseYear AS 'Release Year',
                            Movies.rating AS 'Rating', Movies.movieLength AS 'Length (min)', Genres.genreName AS 'Genre', group_concat(Actors.actorName) AS 'Actors',
                            Directors.directorName AS 'Director Name' 
                            FROM Movies
                            LEFT JOIN Genres ON Movies.idGenre = Genres.idGenre
                            LEFT JOIN Directors ON Movies.idDirector = Directors.idDirector
                            LEFT JOIN Actors_has_Movies ON Movies.idMovie = Actors_has_Movies.idMovie
                            LEFT JOIN Actors ON Actors_has_Movies.idActor = Actors.idActor
                            WHERE releaseYear = %s
                            GROUP BY Movies.movieName
                            ORDER BY Movies.movieName ASC;"""
            data = db.execute_query(db_connection, query1, (releaseYear,)).fetchall()

            # mySQL query to grab director id/name data for our dropdown
            query2 = "SELECT idDirector, directorName FROM Directors"
            director_data = db.execute_query(db_connection, query2).fetchall()

            # mySQL query to grab genre id/name data for our dropdown
            query3 = "SELECT idGenre, genreName FROM Genres"
            genre_data = db.execute_query(db_connection, query3).fetchall()

            # mySQL query to year data for our dropdown
            query4 = """SELECT DISTINCT releaseYear FROM Movies
                        ORDER BY releaseYear ASC;"""
            year_data = db.execute_query(db_connection, query4).fetchall()

            # render movies page passing our query data
            return render_template("search_movies.j2", data=data, directors=director_data, genres=genre_data, years=year_data)

        if request.form.get("Show_All"):
            return redirect("/search_movies")

    # Grab movies data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the movies in Movies
        query1 = """SELECT Movies.idMovie AS 'ID', Movies.movieName AS 'Movie name', Movies.releaseYear AS 'Release Year',
            Movies.rating AS 'Rating', Movies.movieLength AS 'Length (min)', Genres.genreName AS 'Genre', group_concat(Actors.actorName) AS 'Actors',
            Directors.directorName AS 'Director Name' 
            FROM Movies
            LEFT JOIN Genres ON Movies.idGenre = Genres.idGenre
            LEFT JOIN Directors ON Movies.idDirector = Directors.idDirector
            LEFT JOIN Actors_has_Movies ON Movies.idMovie = Actors_has_Movies.idMovie
            LEFT JOIN Actors ON Actors_has_Movies.idActor = Actors.idActor
            GROUP BY Movies.movieName
            ORDER BY Movies.movieName ASC;"""

        data = db.execute_query(db_connection, query1).fetchall()

        # mySQL query to grab director id/name data for our dropdown
        query2 = "SELECT idDirector, directorName FROM Directors"
        director_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab genre id/name data for our dropdown
        query3 = "SELECT idGenre, genreName FROM Genres"
        genre_data = db.execute_query(db_connection, query3).fetchall()

        # mySQL query to year data for our dropdown
        query4 = """SELECT DISTINCT releaseYear FROM Movies
                    ORDER BY releaseYear ASC;"""
        year_data = db.execute_query(db_connection, query4).fetchall()

        # render movies page passing our query data
        return render_template("search_movies.j2", data=data, directors=director_data, genres=genre_data, years=year_data)


@app.route('/directors', methods=["POST", "GET"])
def directors():
    # Separate out the request methods, in this case this is for a POST
    # insert a director into the Directors table
    if request.method == "POST":
        # fire off if user presses the Add Director button
        if request.form.get("Add_Director"):
            # grab user form inputs
            directorName = request.form["directorName"]
            age = request.form["age"]

            query = "INSERT INTO Directors (directorName, age) VALUES (%s,%s)"
            db.execute_query(db_connection, query, (directorName, age))

            # redirect back to people page
            return redirect("/directors")

    # Grab director data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the directors in Directors along with their counts
        query1 = """SELECT idDirector AS 'ID', directorName AS 'Director Name', age AS 'Age',
        (SELECT COUNT(idDirector) FROM Movies WHERE Movies.idDirector = Directors.idDirector GROUP BY idDirector) AS '# Directed',
        (SELECT COUNT(idDirector) FROM Directors_has_Genres WHERE Directors_has_Genres.idDirector = Directors.idDirector GROUP BY idDirector) AS '# Genres Directed'
        FROM Directors;
        """

        data = db.execute_query(db_connection, query1).fetchall()

        # render movies page passing our query data
        return render_template("directors.j2", data=data)

# route for edit functionality, updating the attributes of a movie in Movies
# similar to our delete route, we want to the pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/edit_directors/<int:id>", methods=["POST", "GET"])
def edit_directors(id):
    if request.method == "GET":
        # mySQL query to grab the info of the director with our passed id
        query = "SELECT * FROM Directors WHERE idDirector = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # render edit_directors page passing our query data to the edit_directors template
        return render_template("edit_directors.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Director' button
        if request.form.get("Edit_Directors"):
            # grab user form inputs
            idDirector = request.form["idDirector"]
            directorName = request.form["directorName"]
            age = request.form["age"]

            query = "UPDATE Directors SET Directors.directorName = %s, Directors.age = %s WHERE Directors.idDirector = %s"
            db.execute_query(db_connection, query, (directorName, age, idDirector))

            # redirect back to Directors page after we execute the update query
            return redirect("/directors")

# route for delete functionality, deleting a director from Directors,
# we want to pass the 'id' value of that director on button click (see HTML) via the route
@app.route("/delete_directors/<int:id>")
def delete_directors(id):
    # mySQL query to delete the director with our passed id
    query = "DELETE FROM Directors WHERE idDirector = '%s';"
    db.execute_query(db_connection, query, (id,))

    # redirect back to directors page
    return redirect("/directors")


@app.route('/actors', methods=["POST", "GET"])
def actors():
    # Separate out the request methods, in this case this is for a POST
    # insert an actor into the Actors table
    if request.method == "POST":
        # fire off if user presses the Add Director button
        if request.form.get("Add_Actor"):
            # grab user form inputs
            actorName = request.form["actorName"]
            age = request.form["age"]


            query = "INSERT INTO Actors (actorName, age) VALUES (%s,%s)"
            db.execute_query(db_connection, query, (actorName, age))

            # redirect back to actor page
            return redirect("/actors")

    # Grab actor data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the actors in Actors along with their counts
        query1 = """SELECT idActor AS 'ID', actorName AS 'Actor Name', age AS 'Age',
        (SELECT COUNT(idActor) FROM Actors_has_Movies WHERE Actors_has_Movies.idActor = Actors.idActor GROUP BY idActor) AS '# of Movies Acted in',
        (SELECT COUNT(idActor) FROM Genres_has_Actors WHERE Genres_has_Actors.idActor = Actors.idActor GROUP BY idActor) AS '# of Genres Acted in'
        FROM Actors;
        """
        
        data = db.execute_query(db_connection, query1).fetchall()

        # render actors page passing our query data
        return render_template("actors.j2", data=data)

# route for edit functionality, updating the attributes of an actor in Actors
# similar to our delete route, we want to the pass the 'id' value of that actor on button click (see HTML) via the route
@app.route("/edit_actors/<int:id>", methods=["POST", "GET"])
def edit_actors(id):
    if request.method == "GET":
        # mySQL query to grab the info of the actor with our passed id
        query = "SELECT * FROM Actors WHERE idActor = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # render edit_actors page passing our query data to the edit_actors template
        return render_template("edit_actors.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Actor' button
        if request.form.get("Edit_Actors"):
            # grab user form inputs
            idActor = request.form["idActor"]
            actorName = request.form["actorName"]
            age = request.form["age"]

            query = "UPDATE Actors SET Actors.actorName = %s, Actors.age = %s WHERE Actors.idActor = %s"
            db.execute_query(db_connection, query, (actorName, age, idActor))

            # redirect back to Actors page after we execute the update query
            return redirect("/actors")

# route for delete functionality, deleting an actor from Actors,
# we want to pass the 'id' value of that actor on button click (see HTML) via the route
@app.route("/delete_actors/<int:id>")
def delete_actors(id):
    # mySQL query to delete the actor with our passed id
    query = "DELETE FROM Actors WHERE idActor = '%s';"
    db.execute_query(db_connection, query, (id,))

    # redirect back to actors page
    return redirect("/actors")


@app.route('/genres', methods=["POST", "GET"])
def genres():
    # Separate out the request methods, in this case this is for a POST
    # insert a genre into the Genres table
    if request.method == "POST":
        # fire off if user presses the Add Genre button
        if request.form.get("Add_Genre"):
            # grab user form inputs
            genreName = request.form["genreName"]
            genreName = (genreName,)

            query = "INSERT INTO Genres (genreName) VALUES (%s)"
            db.execute_query(db_connection, query, (genreName,))

            # redirect back to genres page
            return redirect("/genres")

    # Grab genre data so we can send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the genres in Genres along with their counts
        query1 = """SELECT idGenre AS 'ID', genreName AS 'Current Genres',
        (SELECT Count(idGenre) FROM Movies WHERE Movies.idGenre = Genres.idGenre GROUP BY idGenre) AS 'Genre Count'
        FROM Genres;
        """

        data = db.execute_query(db_connection, query1).fetchall()

        # render genres page passing our query data
        return render_template("genres.j2", data=data)

# route for edit functionality, updating the attributes of an genre in Genres
# similar to our delete route, we want to the pass the 'id' value of that genre on button click (see HTML) via the route
@app.route("/edit_genre/<int:id>", methods=["POST", "GET"])
def edit_genres(id):
    if request.method == "GET":
        # mySQL query to grab the info of the genre with our passed id
        query = "SELECT * FROM Genres WHERE idGenre = %s" % (id)

        data = db.execute_query(db_connection, query).fetchall()

        # render edit_genres page passing our query data to the edit_genres template
        return render_template("edit_genres.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Genre' button
        if request.form.get("Edit_Genres"):
            # grab user form inputs
            idGenre = request.form["idGenre"]
            genreName = request.form["genreName"]

            query = "UPDATE Genres SET Genres.genreName = %s WHERE Genres.idGenre = %s"
            
            db.execute_query(db_connection, query, (genreName, idGenre))

            # redirect back to Genres page after we execute the update query
            return redirect("/genres")

# route for delete functionality, deleting an genre from Genres,
# we want to pass the 'id' value of that actor on button click (see HTML) via the route
@app.route("/delete_genre/<int:id>")
def delete_genres(id):
    # mySQL query to delete the genre with our passed id
    query = "DELETE FROM Genres WHERE idGenre = '%s';"
    db.execute_query(db_connection, query, (id,))

    # redirect back to genres page
    return redirect("/genres")

@app.route('/movie_actors', methods=["POST", "GET"])
def movie_actors():
    # Separate out the request methods, in this case this is for a POST
    # insert an actor into the Actors table
    if request.method == "POST":
        # fire off if user presses the Add Director button
        if request.form.get("Add_MovieActor"):
            # grab user form inputs
            idActor = request.form["idActor"]
            idMovie = request.form["idMovie"]

            query = "INSERT INTO Actors_has_Movies (idActor, idMovie) VALUES (%s,%s)"

            db.execute_query(db_connection, query, (idActor, idMovie))

            # redirect back to movie_actors page
            return redirect("/movie_actors")

    # Grab actor data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the actors in Actors along with their counts
        query1 = """SELECT Movies.idMovie AS 'MovieID', Movies.movieName AS "Movie Name", Actors.idActor AS 'ActorID', Actors.actorName AS 'Actor Name'
        FROM Movies
        JOIN Actors_has_Movies ON Movies.idMovie = Actors_has_Movies.idMovie
        JOIN Actors ON Actors_has_Movies.idActor = Actors.idActor
        ORDER BY 'MovieID' ASC;
        """
        data = db.execute_query(db_connection, query1).fetchall()

        # mySQL query to grab movie id/name data for our dropdown
        query2 = "SELECT idMovie, movieName FROM Movies"

        movie_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab actor id/name data for our dropdown
        query3 = "SELECT idActor, actorName FROM Actors"

        actor_data = db.execute_query(db_connection, query3).fetchall()

        # render  page movies_has_actors passing our query data
        return render_template("movie_actors.j2", data=data, movies=movie_data, actors=actor_data)

# route for delete functionality, deleting an actor/movie from Actors_has_Movies,
# we want to pass the 'id' value of that movie actor on button click (see HTML) via the route
@app.route("/delete_movie_actors/<int:idMovie>/<int:idActor>")
def delete_movie_actors(idMovie, idActor):
    # mySQL query to delete the director with our passed id
    query = "DELETE FROM Actors_has_Movies WHERE idMovie = '%s' AND idActor = '%s';"
    db.execute_query(db_connection, query, (idMovie, idActor))

    # redirect back to directors page
    return redirect("/movie_actors")


@app.route('/genre_directors', methods=["POST", "GET"])
def genre_directors():
    # Separate out the request methods, in this case this is for a POST
    # insert an actor into the Actors table
    if request.method == "POST":
        # fire off if user presses the Add Director button
        if request.form.get("Add_GenreDirector"):
            # grab user form inputs
            idGenre = request.form["idGenre"]
            idDirector = request.form["idDirector"]

            query = "INSERT INTO Directors_has_Genres (idGenre, idDirector) VALUES (%s,%s)"
            db.execute_query(db_connection, query, (idGenre, idDirector))

            # redirect back to actor page
            return redirect("/genre_directors")

    # Grab actor data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the actors in Actors along with their counts
        query1 = """SELECT Directors.idDirector AS 'DirectorID', Directors.directorName AS 'Director Name', Genres.idGenre AS 'GenreID', Genres.genreName AS 'Genre'
        FROM Directors
        JOIN Directors_has_Genres ON Directors.idDirector = Directors_has_Genres.idDirector
        JOIN Genres ON Directors_has_Genres.idGenre = Genres.idGenre
        ORDER BY 'Director ID' ASC;
        """
        data = db.execute_query(db_connection, query1).fetchall()

        # mySQL query to grab director id/name data for our dropdown
        query2 = "SELECT idDirector, directorName FROM Directors"
        director_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab actor id/name data for our dropdown
        query3 = "SELECT idGenre, genreName FROM Genres"
        genre_data = db.execute_query(db_connection, query3).fetchall()

        # render actors page passing our query data
        return render_template("genre_directors.j2", data=data, directors=director_data, genres=genre_data)

# route for delete functionality, deleting a genre director/genre from Directors_has_Genres,
# we want to pass the 'id' value of that movie actor on button click (see HTML) via the route
@app.route("/delete_genre_directors/<int:idDirector>/<int:idGenre>")
def delete_genre_directors(idDirector, idGenre):
    # mySQL query to delete the director with our passed id
    query = "DELETE FROM Directors_has_Genres WHERE idDirector = '%s' AND idGenre = '%s';"
    db.execute_query(db_connection, query, (idDirector, idGenre))

    # redirect back to directors page
    return redirect("/genre_directors")


@app.route('/genre_actors', methods=["POST", "GET"])
def genre_actors():
    # Separate out the request methods, in this case this is for a POST
    # insert an actor into the Actors table
    if request.method == "POST":
        # fire off if user presses the Add Director button
        if request.form.get("Add_GenreActor"):
            # grab user form inputs
            idActor = request.form["idActor"]
            idGenre = request.form["idGenre"]

            query = "INSERT INTO Genres_has_Actors (idActor, idGenre) VALUES (%s,%s)"
            db.execute_query(db_connection, query, (idActor, idGenre))

            # redirect back to actor page
            return redirect("/genre_actors")

    # Grab actor data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the actors in Actors along with their counts
        query1 = """SELECT Genres.idGenre AS 'GenreID', Genres.genreName AS 'Genre', Actors.idActor AS 'ActorID', Actors.actorName AS 'Actor Name'
        FROM Genres
        JOIN Genres_has_Actors ON Genres.idGenre = Genres_has_Actors.idGenre
        JOIN Actors ON Genres_has_Actors.idActor = Actors.idActor
        ORDER BY 'Genre ID' ASC;
        """
        data = db.execute_query(db_connection, query1).fetchall()

        # mySQL query to grab director id/name data for our dropdown
        query2 = "SELECT idActor, actorName FROM Actors"
        actor_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to grab actor id/name data for our dropdown
        query3 = "SELECT idGenre, genreName FROM Genres"
        genre_data = db.execute_query(db_connection, query3).fetchall()

        # render actors page passing our query data
        return render_template("genre_actors.j2", data=data, actors=actor_data, genres=genre_data)

# route for delete functionality, deleting a genre/actor from Genres_has_Actors,
# we want to pass the 'id' value of that movie actor on button click (see HTML) via the route
@app.route("/delete_genre_actors/<int:idActor>/<int:idGenre>")
def delete_genre_actors(idActor, idGenre):
    # mySQL query to delete the director with our passed id
    query = "DELETE FROM Genres_has_Actors WHERE idActor = '%s' AND idGenre = '%s';"
    db.execute_query(db_connection, query, (idActor, idGenre))

    # redirect back to directors page
    return redirect("/genre_actors")


# Listener

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=9988, debug=True)
    # app.run(host="flip3.engr.oregonstate.edu", port=9988, debug=False)
    app.run(host="0.0.0.0", port=9988)
