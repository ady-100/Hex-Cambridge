# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 19:00:14 2021

@author: Hex Cambridge

"""

from flask import redirect, render_template, request, session
from functools import wraps
import csv


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


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


def colourcode(value):
    if value > 50:
        return "Red"
    elif value > 40:
        return "Orange"
    else:
        return "Green"
    
def FinancialAnalytics(transactions):
    for item in transactions:
        username = item['username']
        value = item['value']
        datetime = item['date']
        tag = item['tag']

        mean_value = round(mean(value))
        med_value = round(median(value))
    
