DROP TABLE IF EXISTS Plays_For;
CREATE TABLE Plays_For (
  UserID INTEGER REFERENCES User(UserID),
  TeamID INTEGER REFERENCES Team(TeamID),
  Number Integer,
  Position Text,
  Joined Boolean,
  PRIMARY KEY (UserID, TeamID)
);

DROP TABLE IF EXISTS Coaches;
CREATE TABLE Coaches (
  UserID INTEGER REFERENCES User(UserID),
  TeamID INTEGER REFERENCES Team(TeamID),
  PRIMARY KEY (UserID, TeamID)
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
  TeamID REFERENCES Team(TeamID),
  TypeID REFERENCES Type(TypeID)
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
  UserID INTEGER REFERENCES User(UserID),
  ContactID INTEGER REFERENCES Contact(ContactID),
  PRIMARY KEY (UserID, ContactID)
);

DROP TABLE IF EXISTS Equipment;
CREATE TABLE Equipment (
  EquipmentID Integer PRIMARY KEY,
  LoanerID INTEGER REFERENCES User(UserID),
  BorrowerID INTEGER REFERENCES User(UserID),
  Kind Text,
  LoanDate DateTime DEFAULT (datetime('now', 'localtime'))
);

DROP TABLE IF EXISTS User;
CREATE TABLE User (
  UserID Integer PRIMARY KEY,
  Name Text NOT NULL,
  Password Text NOT NULL
);
