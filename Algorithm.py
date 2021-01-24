"""
Created on Sat Jan 23 15:27:54 2021

@author: Earthshot

Title: Algorithm to save the world
"""

import csv

# Inputs
country = 
material1 = 
percent1 = 
material2 = 
percent2 = 
cost = 
weight = 


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

envmat = (((mat_data[material1][0])*percent1)+((mat_data[material2][0])*percent2)) * weight/100
envco = weight * 150e-6 * (co_data[country][4])

Environ = envmat + envco 

print(Environ)


# Ethical Score

ethmat = 0
ethco = weight*((0.5)*((co_data[country][0])/15)+(2/9)*((1-co_data[country][1]+co_data[country][2]+co_data[country][3])/100))*100
Ethical = ethmat + ethco


# Final Score
Score = Ethical/10 + 100/Environ
print(Score)

# Score per kg
kgscore = Score/weight
print(kgscore)

# Price per weight adjusted score
cost_effectivness = kgscore/cost
print(cost_effectivness)

def colourcode(value):
    if value > 10:
        return "Green"
    elif value > 6:
        return "Orange"
    else:
        return "Red"
    
print(colourcode(kgscore))
