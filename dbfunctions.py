import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for
import wtforms

import os

DATABASE = 'db.sqlite'


# Connect to the database.
def connect_db(db_path):
    if db_path is None:
        db_path = os.path.join(os.getcwd(), DATABASE)
    if not os.path.isfile(db_path):
        raise RuntimeError("Can't find database file '{}'".format(db_path))
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


# Open a database connection and hang on to it in the global object.
def open_db_connection(db_path=None):
    g.db = connect_db(db_path)


# If the database is open, close it.
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def add_event(team_id, event_type, date_time, location):
    query = '''
        INSERT INTO Event ( DateTime, Location, TeamID, TypeID) VALUES (:date_time, :location, :team_id, :event_type)
        '''
    cursor = g.db.execute(query, {'team_id': team_id, 'event_type': event_type, 'date_time': date_time,
                                  'location': location})
    g.db.commit()
    return cursor.rowcount
