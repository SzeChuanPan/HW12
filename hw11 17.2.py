import os
import sqlite3

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use a relative path to the database file
database_path = os.path.join(script_dir, 'books.db')  # Remove 'ch17' from the path

# Check if the file exists
if not os.path.isfile(database_path):
    print(f"Error: File not found at {database_path}")
    exit()

# Connect to the database
try:
    connection = sqlite3.connect(database_path)
    print("Connected to the database.")
except sqlite3.OperationalError as e:
    print(f"Error: Unable to connect to the database. {e}")
    exit()

# Rest of the script...



# Create a cursor
cursor = connection.cursor()

# Execute the query to select all data from the titles table
cursor.execute("SELECT * FROM titles")

# Get metadata about the query results
column_names = [description[0] for description in cursor.description]

# Fetch all rows of data
data = cursor.fetchall()

# Display the data in tabular format
print("{:<15} {:<30} {:<10} {:<10}".format(*column_names))  # Header
for row in data:
    print("{:<15} {:<30} {:<10} {:<10}".format(*row))

# Close the cursor and connection
cursor.close()
connection.close()
