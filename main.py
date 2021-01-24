import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import pymysql
import csv

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Set up SQL database
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn1 = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn1

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
        username = request.form.get("username")
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        rows = c.fetchall()
        session["username"] = username
        
        
        # Ensure username exists and password is correct
        password = request.form.get("password")
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
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
    session["loggedin"] = False
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
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        rows = c.fetchall()

        # Ensure username is not taken
        if len(rows) != 0:
            return apology("username is taken", 400)

        # Hash the user's password
        password_hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Add user to database
        c.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, password_hash))

        # Save user address
        address = request.form.get("address")
        c.execute("INSERT INTO locations (username, latitude) VALUES (%s,%s)", (username, address))
        
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
    c.execute("SELECT * FROM users WHERE username = %s", (username,))
    rows = c.fetchall()
    
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

def colourcode(value):
    if value > 50:
        return "Red"
    elif value > 40:
        return "Orange"
    else:
        return "Green"

def Algorithm(country, material1, percent1, material2, percent2, cost, weight):
    with open('Countries_Data.csv', newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',')
        co_data = {}
        for row in csvdata:
            co_data[row[0]] = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]

    with open('Materials_Data.csv', newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',')
        mat_data = {}
        for row in csvdata:
            mat_data[row[0]] = [float(row[1])]
            
    # Environmental Score
    envmat1 = (((mat_data[str(material1)][0])*percent1)+((mat_data[str(material2)][0])*percent2))
    envmat = envmat1*weight/100
    envco = weight * 150e-6 * (co_data[country][4])
    Environ = round(envmat + envco,2) 

    # Ethical Score

    ethmat = 0
    ethco = weight*((0.5)*((co_data[country][0])/15)+(2/9)*((1-co_data[country][1]+co_data[country][2]+co_data[country][3])/100))*100
    Ethical = round(ethmat + ethco,2)

    # Final Score
    Score = round(Environ + 200*weight/Ethical,2)

    # Score per kg
    kgscore = round(Score/weight,2)

    # Price per weight adjusted score
    real_cost = round(float(cost) + Environ * 0.04 + 5*weight/Ethical ,2)
    colour = colourcode(kgscore)
    Al = [Environ, Ethical, Score, kgscore, real_cost, colour]
    
    return Al



@app.route('/data', methods=['POST'])
def data():
    # get data from the test HTML form, at URL /test_form, sending data to /data using the below python
    countrypy = request.form['country']
    material1py = request.form['material1']
    percent1py = float(request.form['percent1'])
    material2py = request.form['material2']
    percent2py = float(request.form['percent2'])
    costpy = float(request.form['cost'])
    weightpy = float(request.form['weight'])

    A = Algorithm(countrypy, material1py, percent1py, material2py, percent2py, costpy, weightpy)
		
    if A[5] == "Green":
        colourimg = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Dark_green.svg/1200px-Dark_green.svg.png"
    elif A[5] == "Orange":
        colourimg = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAA1BMVEX/XgA92nntAAAASElEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIC3AcUIAAFkqh/QAAAAAElFTkSuQmCC"
    else:
        colourimg = "https://professionals.tarkett.com/media/img/M/TH_3917011_3707003_3708011_3912011_3914011_800_800.jpg"

    return render_template("data.html", output1=A[0], output2=A[1], output3=A[2], output4=A[3], output5=A[4], output6=colourimg)

@app.route('/dataadd', methods=['POST'])
def dataadd():
    # get data from the test HTML form, at URL /productadd, sending data to /dataadd using the below python
    pronamepy = request.form['proname']
    countrypy = request.form['country']
    material1py = request.form['material1']
    percent1py = float(request.form['percent1'])
    material2py = request.form['material2']
    percent2py = float(request.form['percent2'])
    costpy = float(request.form['cost'])
    weightpy = float(request.form['weight'])

    A = Algorithm(countrypy, material1py, percent1py, material2py, percent2py, costpy, weightpy)

    return render_template("dataadd.html", output1=A[0], output2=A[1], output3=A[2], output4=A[3], output5=A[4], output6=A[5], output7=pronamepy)


@app.route("/products")
def products():
    """Show list of products"""
    
    conn = open_connection()
    c = conn.cursor()
    
    username = session["username"]
    c.execute("SELECT * FROM products WHERE username = %s", (username,))
    productlist = c.fetchall()
    product_list_display = []
    
    for item in productlist:
        productname = item["productname"]
        cost = item["cost"]
        country = item["country"]
        material1 = item["material1"]
        percentage1 = item["percentage1"]
        material2 = item["material2"]
        percentage2 = item["percentage2"]
        weight = item["weight"]
        score = item["score"]
        colour = colourcode(float(score)/float(weight))
        
        an_item = dict(productname = productname, cost= cost, country= country, material1= material1, percentage1= percentage1, material2= material2, percentage2= percentage2, weight= weight, score= score, colour= colour)
        product_list_display.append(an_item)
        
    # Save commit
    conn.commit()
    conn.close()
    
    return render_template("products.html", product_list_display = product_list_display)

@app.route("/productadd", methods=['GET','POST'])
def productadd():
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        conn = open_connection()
        c = conn.cursor()
        productname = request.form['productname']
        countrypy = request.form['country']
        material1py = request.form['material1']
        percent1py = float(request.form['percent1'])
        material2py = request.form['material2']
        percent2py = float(request.form['percent2'])
        costpy = float(request.form['cost'])
        weightpy = float(request.form['weight'])
    
        A = Algorithm(countrypy, material1py, percent1py, material2py, percent2py, costpy, weightpy)
        
        # Add user to database
        username = session["username"]
        c.execute("INSERT INTO products (username, productname, country, material1, percentage1, material2, percentage2, cost, weight, score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, productname, countrypy, material1py, percent1py, material2py, percent2py, costpy, weightpy, A[2]))
        
        # Save commit
        conn.commit()
        conn.close()
        
        # Redirect user to login page if username is valid
        return redirect("/products")
        
    else:
        return render_template('productadd.html')

@app.route("/contact")
def contact_py():
    return render_template('contact.html')

@app.route('/query', methods=['POST'])
def query():
# get data from the contact HTML form, at URL /contact, sending data to /query using the below python
    querypy = request.form['query']
    emailpy = request.form['email']
    return render_template("query.html", output1=querypy, output2=emailpy)

@app.route("/map")
def map():
    conn = open_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM locations")
    productlist = c.fetchall()
    company_list = []
    
    for item in productlist:
        username = item['username']
        address = item['latitude']
        an_item = dict(companyname = username, address = address)
        company_list.append(an_item)
        
    # Save commit
    conn.commit()
    conn.close()
    
    return render_template("map.html", company_list = company_list)


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
