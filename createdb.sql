
DROP TABLE IF EXISTS Plays_For;
CREATE TABLE Plays_For (
  Email INTEGER REFERENCES User(Email),
  TeamID INTEGER REFERENCES Team(TeamID),
  Number Integer,
  Position Text,
  Joined Boolean,
  PRIMARY KEY (Email, TeamID)
);

DROP TABLE IF EXISTS Coaches;
CREATE TABLE Coaches (
  Email INTEGER REFERENCES User(Email),
  TeamID INTEGER REFERENCES Team(TeamID),
  PRIMARY KEY (Email, TeamID)
);

DROP TABLE IF EXISTS Team;
CREATE TABLE Team (
  TeamID Integer PRIMARY KEY,
  Name Text NOT NULL
);

DROP TABLE IF EXISTS Event;
CREATE TABLE Event (
  EventID Integer PRIMARY KEY,
  Title TEXT NOT NULL,
  DateTime DateTime NOT NULL,
  Location Text,
  TeamID INTEGER REFERENCES Team(TeamID),
  TypeID INTEGER REFERENCES Type(TypeID)
);

DROP TABLE IF EXISTS Event_Type;
CREATE TABLE Event_Type (
  TypeID Integer PRIMARY KEY,
  Description Text NOT NULL
);

DROP TABLE IF EXISTS Notified_For;
CREATE TABLE Notified_For (
  ContactID INTEGER REFERENCES Contact(ContactID),
  TypeID INTEGER REFERENCES Event_Type(TypeID),
  NotificationTime Text NOT NULL,
  PRIMARY KEY (ContactID, TypeID)
);

DROP TABLE IF EXISTS Contact;
CREATE TABLE Contact (
  ContactID Integer,
  Contact Text NOT NULL,
  isPhone Boolean NOT NULL,
  PRIMARY KEY (ContactID, Contact)
);

DROP TABLE IF EXISTS Uses;
CREATE TABLE Uses (
  Email INTEGER REFERENCES User(Email),
  ContactID INTEGER REFERENCES Contact(ContactID),
  PRIMARY KEY (Email, ContactID)
);

DROP TABLE IF EXISTS Equipment;
CREATE TABLE Equipment (
  EquipmentID Integer PRIMARY KEY,
  LoanerID INTEGER REFERENCES User(Email),
  BorrowerID INTEGER REFERENCES User(Email),
  Kind Text,
  LoanDate DateTime DEFAULT (datetime('now', 'localtime'))
);

DROP TABLE IF EXISTS User;
CREATE TABLE User (
  Email Text NOT NULL PRIMARY KEY,
  First_Name Text NOT NULL,
  Last_Name Text NOT NULL,
  Password Text NOT NULL
);

DROP TABLE IF EXISTS Attending_Event;
CREATE TABLE Attending_Event (
  Email Text REFERENCES User (Email),
  EventID Integer REFERENCES Event (EventID),
  Attending Boolean,
  PRIMARY KEY (Email, EventID)
);
