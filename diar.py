import click
import numpy as np
from pathlib import Path
import os
import sqlite3 as sql
import datetime

diarname = 'diarpy.db'

def connect_db():
    conn = sqlite3.connect(diarname)
    c = conn.cursor()
    return c

def setup_db(c):
    c.execute('''CREATE TABLE entry (
              id INTEGER PRIMARY KEY,
              Date date,
              Title text,
              Entry text
              )''')

def add_entry(c, date, title, text):
    c.execute("INSERT INTO entry (date, title, entry) VALUES (?, ?, ?)",
              (date, title, text))

@click.command()
@click.argument('text', required=True, nargs=-1)
def diar(text):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/' + diarname
    exist = os.path.exists(file_path)
    cur = connect_db()
    date = datetime.datetime.now()
    if exist:
        cur = connect_db()
        add_entry(cur, date, 'aaa', text)
    else:
        click.echo('Your diary will be stored in:' + file_path)
        cur = connect_db()
        setup_db(cur)
        add_entry(cur, date, 'aaa', text)

if __name__ == '__main__':
    diar()
