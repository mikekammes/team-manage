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
    query = '''
        SELECT * FROM Event NATURAL JOIN Team NATURAL JOIN Event_Type ORDER BY TeamID
    '''
    cursor = g.db.execute(query)
    g.db.commit()

    return cursor


def add_team(team_name, coach_email):
    cursor = g.db.cursor()
    team_query = '''
        INSERT INTO Team ( Name ) VALUES (:team_name)
    '''
    cursor.execute(team_query, {'team_name': team_name})
    team_row = cursor.lastrowid
    teamid = g.db.execute('SELECT TeamID FROM Team WHERE ROWID = :row', {'row': team_row})
    coaches_query = '''
        INSERT INTO Coaches VALUES (:coach_email, :team_id)
    '''
    cursor.execute(coaches_query, {'coach_email': coach_email, 'team_id': teamid})
    g.db.commit()
    return cursor.rowcount, teamid


def get_players_for_team(team_id):
    query = '''
        SELECT * FROM Plays_For NATURAL JOIN Team WHERE TeamID = :team_id AND Joined
    '''
    cursor = g.db.execute(query, {'team_id': team_id})
    g.db.commit()
    return cursor.fetchall()


def create_rsvp(email, event_id):
    cursor = g.db.cursor()
    user_query = '''
            INSERT INTO Attending_Event (Email, EventID, Attending) VALUES (:email, :eventid, 0)
        '''
    cursor.execute(user_query, {'email': email, 'eventid': event_id})
    g.db.commit()
    return cursor.rowcount


def get_all_players():
    query = '''
        SELECT * FROM "User" NATURAL JOIN Plays_For NATURAL JOIN Team
    '''
    cursor = g.db.execute(query)
    g.db.commit()
    return cursor.fetchall()


def add_players(team_id, email, fname, lname, number, position):
    cursor = g.db.cursor()
    user_query = '''
        INSERT INTO "User" ( Email, First_Name, Last_Name, Password ) VALUES (:email, :fname, :lname, 'pass')
    '''
    cursor.execute(user_query, {'email': email, 'fname': fname, 'lname': lname})
    plays_query = '''
        INSERT INTO Plays_For VALUES (:email, :team_id, :num, :pos, NULL)
    '''
    cursor.execute(plays_query, {'email': email, 'team_id': team_id, 'num': number, 'pos': position})
    g.db.commit()
    return cursor.rowcount


def add_event(title, team_id, event_type, date_time, location):
    cursor = g.db.cursor()
    query = '''
        INSERT INTO Event ( Title, DateTime, Location, TeamID, TypeID) VALUES (:title, :date_time, :location, :team_id, :event_type)
        '''
    cursor.execute(query, {'title': title, 'team_id': team_id, 'event_type': event_type, 'date_time': date_time,
                                  'location': location})
    event_row = cursor.lastrowid
    event_cur = g.db.execute('SELECT EventID FROM Event WHERE ROWID = :row', {'row': event_row})
    event_id = event_cur.fetchone()
    g.db.commit()
    return cursor.rowcount, event_id[0]


def get_all_teams():
    cursor = g.db.execute('SELECT TeamID, Name FROM Team')
    g.db.commit()
    return cursor.fetchall()


def create_user(email, fname, lname):
    cursor = g.db.cursor()
    user_query = '''
        INSERT INTO "User" ( Email, First_Name, Last_Name, Password ) VALUES (:email, :fname, :lname, 'pass')
    '''
    cursor.execute(user_query, {'email': email, 'fname': fname, 'lname': lname})
    g.db.commit()
    return cursor.rowcount


def get_usersname(email):
    cursor = g.db.execute('SELECT First_Name, Last_Name FROM User WHERE email= :email', {'email': email})
    g.db.commit()
    return cursor.fetchone()
