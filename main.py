import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import pymysql

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Set up SQL database

# Create table (removed since already exists)
# c.execute('''CREATE TABLE users
#             (username text, hash text)''')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = 'super secret key'
    
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# The homepage
@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]
    return render_template('index.html', times=dummy_times)

# The about page
@app.route("/about")
def about():
    """Show about us section"""
    return render_template('about.html')
 
# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    conn = open_connection()
    c = conn.cursor()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            print("NoUsername")
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            print("NoPassword")
            return apology("must provide password", 403)

        # Query database for username
        rows = c.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = rows.fetchall()
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][1], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Redirect user to home page
        conn.commit()
        conn.close()
        session["loggedin"] = True
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        conn.commit()
        conn.close()
        return render_template("login.html")

		
# Log Out
@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    loggedin = False
    return redirect("/")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()
    
    conn = open_connection()
    c = conn.cursor()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password is confirmed
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Query database for username
        username = request.form.get("username")
        rows = c.execute("SELECT * FROM users WHERE username = ?", username)
        rows = rows.fetchall()

        # Ensure username is not taken
        if len(rows) != 0:
            return apology("username is taken", 400)

        # Hash the user's password
        password_hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Add user to database
        c.execute("INSERT INTO users ('username', 'hash') VALUES (?,?)", (username, password_hash))

        # Save commit
        conn.commit()
        conn.close()
        
        # Redirect user to login page if username is valid
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Save commit
        conn.commit()
        conn.close()
        return render_template("register.html")
    
@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    
    conn = open_connection()
    c = conn.cursor()
    
    username = request.args.get("username",'')
    rows = c.execute("SELECT * FROM users WHERE username = :name", name=username)
    rows = rows.fetchall()
    
    # Save commit
    conn.commit()
    conn.close()
    
    # Ensure username is not taken
    if len(rows) != 0 or len(username) == 0:
        return jsonify(False), 400
    else:
        return jsonify(True), 200
    

@app.route('/test_form')
def test_form():

    return render_template('test_form.html')

@app.route('/data', methods=['POST'])
def data():
    # get data from the test HTML form, at URL /test_form, sending data to /data using the below python
    countrypy = request.form['country']
    materialpy = request.form['material']
    costpy = request.form['cost']
    weightpy = request.form['weight']
    return render_template("data.html", output1=countrypy, output2=materialpy, output3=costpy, output4=weightpy)
    


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='127.0.0.1', port=8080, debug=True)
