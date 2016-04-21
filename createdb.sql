CREATE TABLE User (
  UserID Integer PRIMARY KEY,
  Name Text NOT NULL,
  RoleID REFERENCES Role(RoleID)
);

CREATE TABLE Plays_For (
  UserID REFERENCES User(UserID),
  TeamID REFERENCES Team(TeamID),
  Number Integer,
  Position Text,
  PRIMARY KEY (UserID, TeamID)
);

CREATE TABLE Coaches (
  UserID REFERENCES User(UserID),
  TeamID REFERENCES Team(TeamID),
  PRIMARY KEY (UserID, TeamID)
);

CREATE TABLE Team (
  TeamID Integer PRIMARY KEY,
  Name Text NOT NULL
);

CREATE TABLE Role (
  RoleID Integer PRIMARY KEY,
  Title Text NOT NULL,
  Description Text
);

CREATE TABLE Event (
  EventID Integer PRIMARY KEY,
  DateTime DateTime NOT NULL,
  Location Text,
  TeamID REFERENCES Team(TeamID),
  TypeID REFERENCES Type(TypeID)
);

CREATE TABLE Event_Type (
  TypeID Integer PRIMARY KEY,
  Description Text NOT NULL
);

CREATE TABLE Notified_For (
  ContactID REFERENCES Contact(ContactID),
  TypeID REFERENCES Event_Type(TypeID),
  NotificationTime Text NOT NULL,
  PRIMARY KEY (ContactID, TypeID)
);

CREATE TABLE Contact (
  ContactID Integer,
  Contact Text NOT NULL,
  isPhone Boolean NOT NULL,
  PRIMARY KEY (ContactID, Contact)
);


CREATE TABLE Uses (
  UserID REFERENCES User(UserID),
  ContactID REFERENCES Contact(ContactID),
  PRIMARY KEY (UserID, ContactID)
);

CREATE TABLE Equipment (
  EquipmentID Integer PRIMARY KEY,
  LoanerID REFERENCES User(UserID),
  BorrowerID REFERENCES User(UserID),
  Kind Text,
  LoanDate DateTime DEFAULT (datetime('now', 'localtime'))
);