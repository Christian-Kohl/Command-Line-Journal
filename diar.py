import click
import numpy as np
from pathlib import Path
import os
import sqlite3
import datetime

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

def add_entry(c, date, title, text):
    print(type(date))
    print(type(title))
    text = ' '.join(text)
    print(type(text))
    c.execute("INSERT INTO entry (date, title, entry) VALUES (?, ?, ?)",
              (date, title, text, ))

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
        date = datetime.datetime.now()
        if exist:
            add_entry(cur, date, 'aaa', text)
        else:
            click.echo('Your diary will be stored in:' + file_path)
            setup_db(cur)
            add_entry(cur, date, 'aaa', text)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    diar()
