# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 19:00:14 2021

@author: Hex Cambridge

"""

from flask import redirect, render_template, request, session
from functools import wraps
import csv
from statistics import mean, median, mode


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
    Environ = round(envmat + envco,1) 

    # Ethical Score

    ethmat = 0
    ethco = weight*((0.5)*((co_data[country][0])/15)+(2/9)*((1-co_data[country][1]+co_data[country][2]+co_data[country][3])/100))*100
    Ethical = round(ethmat + ethco,1)

    # Final Score
    Score = round(Environ + 50*weight*weight/Ethical,1)

    # Score per kg
    kgscore = round(Score/weight,1)

    # Price per weight adjusted score
    real_cost = round(float(cost) + Environ * 0.04 + 10*weight/Ethical ,2)
    colour = colourcode(kgscore)
    Al = [Environ, Ethical, Score, kgscore, real_cost, colour]
    
    return Al


def colourcode(value):
    if value > 55:
        return "Red"
    elif value > 40:
        return "Orange"
    else:
        return "Green"
    
def FinancialAnalytics(transactions):
    valuelist = []
    for item in transactions:
        username = item['username']
        value = item['value']
        datetime = item['date']
        tag = item['tag']
        valuelist.append(value)
        
    # Test data for demonstration purposes
    mean1 = 100
    median1 = 90
    mode1 = 70
    #mean1 = mean(valuelist)
    #median1 = median(valuelist)
    #mode1 = mode(valuelist)
    return [mean1, median1, mode1]
        
    
"""
def EnvironAnalytics(productlistofdict):
    score = []
    for dic in productlistofdict:
        score.append(productlistofdict[dic]['score'])
        # returns list of scores
        
    countries = []
    for dic in productlistofdict:
        countries.append(productlistofdict[dic]['country'])
        # returns list of countries of origin
    
    materials = []
    for dic in productlistofdict:
        materials.append(productlistofdict[dic]['material1'])
        # returns list of major materials
        
    weights = []
    for dic in productlistofdict:
        weights.append(productlistofdict[dic]['weight'])
        # returns list of weights
        
    for i in range(len(score)):
        score[i] = score[i]/weights[i]
     
    # Calculate basic analytics
    mean_score = sum(score) / float(len(score))
    median_score = median(score)
    range = max(score) - min(score)
    Q1_score = np.percentile(data, 25, interpolation = 'midpoint') 
    Q3_score = np.percentile(data, 75, interpolation = 'midpoint') 
    IQR_score = Q3_score - Q1_score
    
    # Read in country data and find distances, then do the same and get basic data on distances. Also return mode of country of origin. 
    
    with open('Countries_Data.csv', newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',')
        co_data = {}
        for row in csvdata:
            co_data[row[0]] = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]
    
    country = []
    for i in countries:
        country.append(co_data[i][4])
    
    mean_country = sum(country) / float(len(country))
    median_country = median(country)
    range_country = max(country) - min(country)
    Q1_country = np.percentile(data, 25, interpolation = 'midpoint') 
    Q3_country = np.percentile(data, 75, interpolation = 'midpoint') 
    IQR_country = Q3_country - Q1_country
    mode_country = mode(countries)
    
    
    # Do the same thing for materials with their CO2 eq. data
    
    with open('Materials_Data.csv', newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',')
        mat_data = {}
        for row in csvdata:
            mat_data[row[0]] = [float(row[1])]
            
    matco2 = []
    for i in materials:
        matco2.append(mat_data[i][0])
    
    mean_matco2 = sum(country) / float(len(country))
    median_matco2 = median(matco2)
    range_matco2 = max(matco2) - min(matco2)
    Q1_matco2 = np.percentile(data, 25, interpolation = 'midpoint') 
    Q3_matco2 = np.percentile(data, 75, interpolation = 'midpoint') 
    IQR_matco2 = Q3_matco2 - Q1_matco2
    mode_matco2 = mode(materials)
    
    
    return [mean_score, range_score, median_score, IQR_score, mean_country, range_country, median_country, IQR_country, mode_country, mean_matco2, range_matco2, median_matco2, IQR_matco2, mode_matco2]
"""
