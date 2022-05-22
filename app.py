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

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_silverbj"
app.config["MYSQL_PASSWORD"] = "2804"
app.config["MYSQL_DB"] = "cs340_silverbj"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


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
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, idDirector))
                mysql.connection.commit()

            # account for null movieLength and idGenre
            elif (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, rating, idDirector) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, idDirector))
                mysql.connection.commit()

            # account for null rating and movieLength
            elif (rating == "" or rating == "None") and (movieLength == "" or movieLength == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, idDirector) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, idDirector))
                mysql.connection.commit()

            # account for null rating and idGenre
            elif (rating == "" or rating == "None") and (idGenre == "" or idGenre == "None"):
                # mySQL query to insert a new movie into Movies with our form inputs
                query = "INSERT INTO Movies (movieName, releaseYear, movieLength, idDirector) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, movieLength, idDirector))
                mysql.connection.commit()

            # account for null rating
            elif rating == "" or rating == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, movieLength, idDirector) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, movieLength, idDirector))
                mysql.connection.commit()

            # account for null movieLength
            elif movieLength == "" or movieLength == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, rating, idDirector) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, idDirector))
                mysql.connection.commit()

            # account for null idGenre
            elif movieLength == "" or movieLength == "None":
                query = "INSERT INTO Movies (movieName, releaseYear, rating, movieLength, idDirector) VALUES (%s, %s,%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, movieLength, idDirector))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Movies (movieName, releaseYear, rating, movieLength, idDirector, idGenre) VALUES (%s, %s,%s,%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, movieLength, idDirector, idGenre))
                mysql.connection.commit()

            # redirect back to people page
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
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()

        # mySQL query to grab actor id/name data for our dropdown
        query2 = "SELECT idActor, actorName FROM Actors"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        actor_data = cur.fetchall()

        # render movies page passing our query data
        return render_template("movies.j2", data=data, actors=actor_data)

# route for edit functionality, updating the attributes of a movie in Movies
# similar to our delete route, we want to the pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/edit_movies/<int:id>", methods=["POST", "GET"])
def edit_movies(id):
    if request.method == "GET":
        # mySQL query to grab the info of the movie with our passed id
        query = "SELECT * FROM Movies WHERE idMovie = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab actor id/name data for our dropdown
        query2 = "SELECT idActor, actorName FROM Actors"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        actor_data = cur.fetchall()

        # render edit_movies page passing our query data to the edit_movies template
        return render_template("edit_movies.j2", data=data, actors=actor_data)

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
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, idDirector, idMovie))
                mysql.connection.commit()

            # account for null rating and idGenre
            elif (rating == "" or rating == "None") and (idGenre == "" or idGenre == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.movieLength = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, movieLength, idDirector, idMovie))
                mysql.connection.commit()

            # account for null movieLength and idGenre
            elif (idGenre == "" or idGenre == "None") and (movieLength == "" or movieLength == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, idDirector, idMovie))
                mysql.connection.commit()

            # account for null movieLength and rating
            elif (idGenre == "" or idGenre == "None") and (rating == "" or rating == "None"):
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, idDirector, idGenre, idMovie))
                mysql.connection.commit()

            # account for null rating
            elif rating == "" or rating == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.movieLength = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, movieLength, idDirector, idGenre, idMovie))
                mysql.connection.commit()

            # account for null movieLength
            elif movieLength == "" or movieLength == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, idDirector, idGenre, idMovie))
                mysql.connection.commit()

            # account for null idGenre
            elif movieLength == "" or movieLength == "None":
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.movieLength = %s, Movies.idDirector = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, movieLength, idDirector, idMovie))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Movies SET Movies.movieName = %s, Movies.releaseYear = %s, Movies.rating = %s, Movies.movieLength = %s, Movies.idDirector = %s, Movies.idGenre = %s WHERE Movies.idMovie = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (movieName, releaseYear, rating, movieLength, idDirector, idGenre, idMovie))
                mysql.connection.commit()

            # redirect back to Movies page after we execute the update query
            return redirect("/movies")

# route for delete functionality, deleting a movie from Movies,
# we want to pass the 'id' value of that movie on button click (see HTML) via the route
@app.route("/delete_movies/<int:id>")
def delete_movies(id):
    # mySQL query to delete the movie with our passed id
    query = "DELETE FROM Movies WHERE idMovie = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/movies")

"""
@app.route('/bsg-people')
def bsg_people():

    # Write the query and save it to a variable
    query = "SELECT * FROM bsg_people;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    #
    # The json.dumps() function simply converts the dictionary that was
    # returned by the fetchall() call to JSON so we can display it on the
    # page.
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("bsg.j2", bsg_people=results)

@app.route('/people', methods=["POST", "GET"])
def people():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Person"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if age == "" and homeworld == "0":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO bsg_people (fname, lname) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "INSERT INTO bsg_people (fname, lname, age) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age))
                mysql.connection.commit()

            # account for null age
            elif age == "":
                query = "INSERT INTO bsg_people (fname, lname, homeworld) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO bsg_people (fname, lname, homeworld, age) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/people")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT bsg_people.id, fname, lname, bsg_planets.name AS homeworld, age FROM bsg_people LEFT JOIN bsg_planets ON homeworld = bsg_planets.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("people.j2", data=data, homeworlds=homeworld_data)

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_people/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM bsg_people WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/people")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_people/<int:id>", methods=["POST", "GET"])
def edit_people(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form["personID"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")

"""

# Listener

if __name__ == "__main__":
    app.run(port=9988, debug=True)
    # port = int(os.environ.get('PORT', 9988))
    # #                                 ^^^^
    # #              You can replace this number with any valid port
    #
    # app.run(port=port, debug=True)