# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 18:39:49 2021

@author: Kieran Dalton

"""
import sqlite3
conn = sqlite3.connect('Database1.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users
             (user text, hash text)''')


# Save (commit) the changes
conn.commit()

