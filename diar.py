import click
import numpy as np
from pathlib import Path
import os
import sqlite3
import datetime
import dateparser as db
import sys

# Setup the name for the database
diarname = 'diarpy.db'


# Function to connect to the database, using sqlite3
def connect_db():
    conn = sqlite3.connect(diarname)
    c = conn.cursor()
    return conn, c


# Sets up the table for entering entries
def setup_db(c):
    c.execute('''CREATE TABLE entry (
              id INTEGER PRIMARY KEY,
              Date date,
              Title text,
              Entry text
              )''')

# Function to add an entry to the database
def add_entry(c, text):
    # Changes the arguments to a string, separated by spaces
    text = ' '.join(text)
    # Checks for colons, to see if there is a title or not
    if ':' in text:
        # Splits the header from the diary entry
        header = text.split(':')[0]
        text = text[len(header)+1:]
        if text[0] == ' ':
            text = text[1:]
        # Extracts the date and title from the header
        date, title = extract_header(header)
    else:
        # If there is no Header then a standard Title and date are used
        date = datetime.datetime.now()
        title = "Journal Entry"
    # Runs the SQL statement to add entry into the database
    c.execute("INSERT INTO entry (date, title, entry) VALUES (?, ?, ?)",
              (date.replace(microsecond=0, second=0, minute=0), title, text, ))

# Manages the command line interface
@click.command()
@click.option('--get', default=False)
@click.argument('text', required=True, nargs=-1)
def diar(get, text):
    # Sets up the filename strings
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/' + diarname
    # Manages the option to retrieve or to add to the database
    if get:
        conn, cur = connect_db()
        x = cur.execute('SELECT * FROM entry')
    else:
        # Check if the file exists
        exist = os.path.exists(file_path)
        conn, cur = connect_db()
        if exist:
            add_entry(cur, text)
        else:
            # Creates a new database to store entries in
            click.echo('Your diary will be stored in:' + file_path)
            setup_db(cur)
            add_entry(cur, text)
    conn.commit()
    conn.close()

# Function to extract the title and date from a header
def extract_header(header):
    # Splits header into date, and title section separated by ','
    sections = header.split(', ')
    #Checks the number of sections
    if len(sections) > 2:
        # Gives the user information before exiting
        click.echo("Sorry, you can't have commas in your title, please try again")
        sys.exit()
    elif len(sections) == 1:
        # Checks whether the single section is a title or a date
        date = db.parse(sections[0])
        if date is None:
            date = datetime.datetime.now()
            title = sections[0]
        else:
            title = 'Journal Entry'
    else:
        # Checks which section is which
        if db.parse(sections[0]) is None:
            date = db.parse(sections[1])
            title = sections[0]
        else:
            date = db.parse(sections[0])
            title = sections[1]
    return date, title


if __name__ == '__main__':
    diar()
