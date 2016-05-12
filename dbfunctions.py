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
        SELECT *
        FROM (
          SELECT*,COUNT(Attending) AS RSVPs
          FROM Event
            NATURAL JOIN Team
            NATURAL JOIN Attending_Event
          GROUP BY EventID
        )
        WHERE TeamID IN (SELECT TeamID FROM Plays_For WHERE Email = :email);
    '''
    cursor = g.db.execute(query, {'email': email})
    g.db.commit()
    return cursor


def get_all_events():
    query = '''
        SELECT *
        FROM (
          SELECT*,COUNT(Attending) AS RSVPs
          FROM Event
            NATURAL JOIN Team
            NATURAL JOIN Attending_Event
          GROUP BY EventID
        );
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
    team_cur = g.db.execute('SELECT TeamID FROM Team WHERE ROWID = :row', {'row': team_row})
    teamid = team_cur.fetchone()[0]
    coaches_query = '''
        INSERT INTO Coaches VALUES (:coach_email, :team_id)
    '''
    cursor.execute(coaches_query, {'coach_email': coach_email, 'team_id': teamid})
    g.db.commit()
    return cursor.rowcount, teamid


def get_players_for_team(team_id):
    query = '''
        SELECT * FROM Plays_For NATURAL JOIN Team NATURAL JOIN User WHERE TeamID = :team_id
    '''
    cursor = g.db.execute(query, {'team_id': team_id})
    g.db.commit()
    return cursor.fetchall()


def create_rsvp(email, event_id):
    cursor = g.db.cursor()
    user_query = '''
            INSERT INTO Attending_Event (Email, EventID, Attending) VALUES (:email, :eventid, NULL )
        '''
    cursor.execute(user_query, {'email': email, 'eventid': event_id})
    g.db.commit()
    return cursor.rowcount


def delete_event(event_id):
    cursor = g.db.cursor()
    g.db.execute('DELETE FROM Attending_Event WHERE EventID = :event_id', {'event_id': event_id})
    g.db.execute('DELETE FROM Event WHERE EventID = :event_id', {'event_id': event_id})
    g.db.commit()
    return cursor.rowcount


def get_all_players():
    query = '''
        SELECT * FROM "User" NATURAL JOIN Plays_For NATURAL JOIN Team
    '''
    cursor = g.db.execute(query)
    g.db.commit()
    return cursor.fetchall()


def player_exists(email):
    cursor = g.db.execute('SELECT COUNT(*) FROM User WHERE Email = :email', {'email': email})
    g.db.commit()
    return cursor.fetchall()


def player_plays_for_team(email, team_id):
    cursor = g.db.execute('SELECT COUNT(*) FROM User INNER JOIN Plays_For ON User.Email = Plays_For.Email WHERE User.Email = :email AND TeamID = :team_id', {'email': email, 'team_id': team_id})
    g.db.commit()
    return cursor.fetchall()


def add_player_and_invite(team_id, email, fname, lname, number, position):
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


def invite_player(team_id, email, number, position):
    cursor = g.db.cursor()
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


def get_emails_from_team(event_id):
    query = '''
        SELECT User.Email FROM User
        INNER JOIN Plays_For ON User.Email = Plays_For.Email
        INNER JOIN Team ON Plays_For.TeamID =Team.TeamID
        INNER JOIN Event ON Event.TeamID = Team.TeamID
        WHERE Event.EventID = :event_id
        ORDER BY User.Email
        '''
    cursor = g.db.execute(query, {'event_id': event_id})
    g.db.commit()
    return cursor.fetchall()


def RSVP(event_id, email, attending_status):
    if attending_status == '0':
        query = '''
            UPDATE attending_event SET Attending = NULL WHERE EventID = :event_id AND Email = :email
        '''
    else:
        query = '''
            UPDATE attending_event SET Attending = :attending WHERE EventID = :event_id AND Email = :email
        '''
    cursor = g.db.execute(query, {'event_id': event_id, 'email': email, 'attending': attending_status})
    g.db.commit()
    return cursor.rowcount


def get_team_invites(email):
    query = '''
        SELECT Team.Name, Team.TeamID
        FROM User
        INNER JOIN Plays_For ON User.Email = Plays_For.Email
        INNER JOIN Team ON Plays_For.TeamID =Team.TeamID
        WHERE User.Email = :email
        '''
    cursor = g.db.execute(query, {'email': email})
    g.db.commit()
    return cursor.fetchall()


def accept_invite(email, team_id, accept_status):
    query = '''
      UPDATE Plays_For SET Joined = :accepting WHERE TeamID = :team_id AND Email = :email
    '''
    cursor = g.db.execute(query, {'team_id': team_id, 'email': email, 'accepting': accept_status})
    g.db.commit()
    return cursor.rowcount


def add_contact(email, is_phone, contact):
    cursor = g.db.cursor()
    user_query = '''
        INSERT INTO "Contact" ( Email, Contact, isPhone ) VALUES (:email, :contact, :is_phone)
    '''

    cursor.execute(user_query, {'email': email, 'contact': contact, 'is_phone': is_phone})
    contact_row = cursor.lastrowid
    contact_cur = g.db.execute('SELECT ContactID FROM Contact WHERE ROWID = :row', {'row': contact_row})
    teamid = contact_cur.fetchone()[0]
    g.db.commit()
    return cursor.rowcount, teamid


def get_event_types():
    cursor = g.db.execute('SELECT TypeID, Description FROM Event_Type')
    g.db.commit()
    return cursor.fetchall()


def setting_exists(contact, type):
    cursor = g.db.execute('SELECT COUNT(*) FROM Notified_for WHERE ContactID = :contact AND TypeID = :type', {'contact': contact, 'type': type})
    g.db.commit()
    return cursor.fetchall()


def create_setting(contact, type_id, time):
    cursor = g.db.cursor()
    user_query = '''
                INSERT INTO Notified_For VALUES (:contact, :type_id, :notification_time )
            '''
    cursor.execute(user_query, {'contact': contact, 'type_id': type_id, 'notification_time': time})
    g.db.commit()
    return cursor.rowcount


def update_setting(contact, type_id, time):
    cursor = g.db.cursor()
    user_query = '''
                UPDATE Notified_For
                SET 'notificationtime' = :notification_time
                WHERE ContactID = :contact AND typeid = type_id
            '''
    cursor.execute(user_query, {'contact': contact, 'type_id': type_id, 'notification_time': time})
    g.db.commit()
    return cursor.rowcount
