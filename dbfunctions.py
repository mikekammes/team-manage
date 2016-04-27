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


def add_event(title, team_id, event_type, date_time, location):
    query = '''
        INSERT INTO Event ( Title, DateTime, Location, TeamID, TypeID) VALUES (:title, :date_time, :location, :team_id, :event_type)
        '''
    cursor = g.db.execute(query, {'title': title, 'team_id': team_id, 'event_type': event_type, 'date_time': date_time,
                                  'location': location})
    g.db.commit()
    return cursor.rowcount

def get_event_for_user(email):
    query = '''
        SELECT * FROM Event NATURAL JOIN Team NATURAL JOIN Plays_For WHERE Email = :email
    '''
    cursor = g.db.execute(query, {'email': email})
    g.db.commit()
    return cursor


def get_all_events():
    print("Getting all userrs")

    query = '''
        SELECT * FROM Event
    '''
    cursor = g.db.execute(query)
    g.db.commit()

    return cursor

def add_team(team_name):
    query = '''
        INSERT INTO Team ( Name ) VALUES (:team_name)
        '''
    # Insert Coaches for
    # Insert Plays for
    cursor = g.db.execute(query, {'team_name': team_name})
    g.db.commit()
    return cursor.rowcount

def get_players_for_team(team_id):
    query = '''
        SELECT * FROM "User" NATURAL JOIN Plays_For WHERE TeamID = :team_id
    '''
    cursor = g.db.execute(query, {'team_id': team_id})
    g.db.commit()
    return cursor


def get_all_players():
    query = '''
        SELECT * FROM "User" NATURAL JOIN Plays_For
    '''
    cursor = g.db.execute(query)
    g.db.commit()
    return cursor

def add_event(team_id, name, email):
    query = '''
        INSERT INTO Event ( Title, DateTime, Location, TeamID, TypeID) VALUES (:title, :date_time, :location, :team_id, :event_type)
        '''
    cursor = g.db.execute(query, {'title': title, 'team_id': team_id, 'event_type': event_type, 'date_time': date_time,
                                  'location': location})
    g.db.commit()
    return cursor.rowcount