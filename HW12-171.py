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
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# a. Select all authors' last names from the authors table in descending order.
cursor.execute('SELECT last FROM authors ORDER BY last DESC')
authors_last_names = cursor.fetchall()
print("Authors' Last Names (Descending Order):", authors_last_names)

# b. Select all book titles from the titles table in ascending order.
cursor.execute('SELECT title FROM titles ORDER BY title ASC')
book_titles = cursor.fetchall()
print("Book Titles (Ascending Order):", book_titles)

# c. Use an INNER JOIN to select all the books for a specific author.
# Include the title, copyright year, and ISBN. Order the information alphabetically by title.
author_name = 'Rick Riordan'  # Percy Jackson's author
cursor.execute('''
    SELECT titles.title, titles.copyright, titles.isbn
    FROM titles
    INNER JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
    INNER JOIN authors ON author_ISBN.id = authors.id
    WHERE authors.first || ' ' || authors.last = ?
    ORDER BY titles.title ASC
''', (author_name,))
author_books = cursor.fetchall()
print(f"Books by {author_name}:", author_books)

# d. Insert a new author into the authors table.
new_author = ('New', 'Author')  # Replace with the actual author's name
cursor.execute('INSERT INTO authors (first, last) VALUES (?, ?)', new_author)
connection.commit()

# ...

# e. Insert a new title for an author.
new_title = ('New Book ISBN', 'New Book Title', 1, '2023')  # Replace with actual values

# Check if the ISBN already exists
cursor.execute('SELECT * FROM titles WHERE isbn = ?', (new_title[0],))
existing_title = cursor.fetchone()

if existing_title:
    # ISBN already exists, update the existing title
    cursor.execute('''
        UPDATE titles
        SET title = ?, edition = ?, copyright = ?
        WHERE isbn = ?
    ''', (new_title[1], new_title[2], new_title[3], new_title[0]))
else:
    # ISBN does not exist, insert the new title
    cursor.execute('INSERT INTO titles (isbn, title, edition, copyright) VALUES (?, ?, ?, ?)', new_title)

connection.commit()

# ...


# Close the connection
connection.close()
