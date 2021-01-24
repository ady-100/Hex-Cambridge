--------------------------------------------------------------------------------
# SQL Cheat Sheet
--------------------------------------------------------------------------------
## Tables

* users has columns: username, password
* locations has columns: username, latitude, longitude
* products has columns: username, country, material1, percentage1, material2, percentage2, cost, weight

--------------------------------------------------------------------------------
## To set up a search (e.g. search for products from username = tesco)

		username = tesco
		conn = open_connection()
		c = conn.cursor()
		c.execute(SELECT * FROM products WHERE username = %s", (username,))
		rows = c.fetchall()
		conn.commit()
       		conn.close()

rows will be a list with [username, country, material1...]. You can then use Flask to send this to a html file, making a list by looping over all of the rows.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
## To write to a database

		lat = 01
		long = 02
		conn = open_connection()
		c = conn.cursor()
        	c.execute("INSERT INTO locations (username, latitude, longitude) VALUES (%s,%s,%s)", (username, lat,long))
		conn.commit()
       		conn.close()
-------------------------------------------------------------------------------
## To perform a more specific search

		username = tesco
		cost = str(90)
		conn = open_connection()
		c = conn.cursor()
		c.execute("SELECT * FROM products WHERE username = %s AND cost = %s", (username, cost))
		searchoutput = c.fetchall() # This could be empty
		conn.commit()
       		conn.close()
		
