
# Create a blank db.sqlite3 for the project
import sqlite3

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')

# Close the connection
conn.close()
