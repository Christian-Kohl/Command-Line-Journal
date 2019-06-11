import click
import numpy as np
from pathlib import Path
import os
import sqlite3
import datetime
import dateparser as db

diarname = 'diarpy.db'

def connect_db():
    conn = sqlite3.connect(diarname)
    c = conn.cursor()
    return conn, c

def setup_db(c):
    c.execute('''CREATE TABLE entry (
              id INTEGER PRIMARY KEY,
              Date date,
              Title text,
              Entry text
              )''')

def add_entry(c, text):
    text = ' '.join(text)
    if ':' in text:
        header = text.split(':')[0]
        text = text[len(header)+1:]
        if text[0] == ' ':
            text = text[1:]
        date, title = extract_header(header)
    else:
        date = datetime.datetime.now().replace(microsecond=0,
                                               second=0,
                                               minute=0)
        title = "Journal Entry"
    print(header)
    print(date)
    c.execute("INSERT INTO entry (date, title, entry) VALUES (?, ?, ?)",
              (date, header, text, ))

@click.command()
@click.option('--get', default=False)
@click.argument('text', required=True, nargs=-1)
def diar(get, text):
    if get:
        conn, cur = connect_db()
        x = cur.execute('SELECT * FROM entry')
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = dir_path + '/' + diarname
        exist = os.path.exists(file_path)
        conn, cur = connect_db()
        if exist:
            add_entry(cur, text)
        else:
            click.echo('Your diary will be stored in:' + file_path)
            setup_db(cur)
            add_entry(cur, date, 'aaa', text)
    conn.commit()
    conn.close()

def extract_header(header):
    sections = header.split(',')
    if len(sections) > 2:
        click.echo("Sorry, you can't have commas in your title, please try again")
    elif len(sections) == 1:
        date = db.parse(sections[0])
        if date is None:
            date = datetime.datetime.now().replace(microsecond=0,
                                                   second=0,
                                                   minute=0)
    else:
        return datetime.datetime.now(), 'Hello'

if __name__ == '__main__':
    diar()
