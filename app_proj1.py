from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import database.db_connector as db
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_harwoodt'
app.config['MYSQL_PASSWORD'] = '7358' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_harwoodt'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    query = "SELECT * FROM Actors;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("bsg.j2", bsg_people=results)

    # # query1 = "SELECT * FROM Actors;"
    # query1 = 'DROP TABLE IF EXISTS diagnostic;';
    # query2 = 'CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);';
    # query3 = 'INSERT INTO diagnostic (text) VALUES ("MySQL is working! -silverbj")';
    # query4 = 'SELECT * FROM diagnostic;';
    # cur = mysql.connection.cursor()
    # cur.execute(query1)
    # cur.execute(query2)
    # cur.execute(query3)
    # cur.execute(query4)
    # results = cur.fetchall()
    #
    # return results[0]


# Listener
if __name__ == "__main__":

    #Start the app on port 9988, it will be different once hosted
    app.run(port=9988, debug=True)