INSERT INTO "Plays_For" VALUES('joel@example.com',1,3,'Handler',1);
INSERT INTO "Plays_For" VALUES('chris@example.com',1,20,'Cutter',1);
INSERT INTO "Plays_For" VALUES('todd@example.com',1,4,'Handler',1);
INSERT INTO "Plays_For" VALUES('mitch@example.com',2,10,'Defense',1);
INSERT INTO "Plays_For" VALUES('mike@example.com',2,14,'Striker',1);


INSERT INTO "Coaches" VALUES('joel@example.com',1);
INSERT INTO "Coaches" VALUES('mitch@example.com',2);

INSERT INTO "Team" VALUES(1,'Yak (TU Frisbee)');
INSERT INTO "Team" VALUES(2,'Trojan Lacrosse');

INSERT INTO "Event_Type" VALUES(1,'Game');
INSERT INTO "Event_Type" VALUES(2,'Practice');
INSERT INTO "Event_Type" VALUES(3,'Workout');
INSERT INTO "Event_Type" VALUES(4,'Team Bonding Event');

INSERT INTO "User" VALUES('joel@example.com','Joel','Bierre','pass');
INSERT INTO "User" VALUES('chris@example.com','Chris','Shelor','pass');
INSERT INTO "User" VALUES('todd@example.com','Todd','Fenstermacher','pass');
INSERT INTO "User" VALUES('mitch@example.com','Mitch','Pawlanta','pass');
INSERT INTO "User" VALUES('mike@example.com','Mike','Kammes','pass');

INSERT INTO "Event" VALUES(1,'Away vs. IWU','2016-05-14 14:30:00','Matter Park',1,1);
INSERT INTO "Event" VALUES(2,'Tuesday practice','2016-05-18 16:00:00','Practice Field',1,2);
INSERT INTO "Event" VALUES(3,'End of year party','2016-05-20 17:00:00','Student Center',1,4);
INSERT INTO "Event" VALUES(4,'Home vs. Purdue','2016-04-25 15:00:00','Lacrosse Field',2,1);
INSERT INTO "Event" VALUES(5,'Walkthrough practice','2016-04-24 14:00:00','Practice Field',2,2);
INSERT INTO "Event" VALUES(6,'Thursday morning workout','2016-04-23 06:30:00','KSAC',2,3);

INSERT INTO "Attending_Event" VALUES('joel@example.com', 1, 1);
INSERT INTO "Attending_Event" VALUES('joel@example.com', 2, NULL);
INSERT INTO "Attending_Event" VALUES('joel@example.com', 3, NULL);
INSERT INTO "Attending_Event" VALUES('chris@example.com', 1, 1);
INSERT INTO "Attending_Event" VALUES('chris@example.com', 2, NULL);
INSERT INTO "Attending_Event" VALUES('chris@example.com', 3, 1);
INSERT INTO "Attending_Event" VALUES('todd@example.com', 1, NULL);
INSERT INTO "Attending_Event" VALUES('todd@example.com', 2, NULL);
INSERT INTO "Attending_Event" VALUES('todd@example.com', 3, 1);
INSERT INTO "Attending_Event" VALUES('mike@example.com', 4, 1);
INSERT INTO "Attending_Event" VALUES('mike@example.com', 5, NULL);
INSERT INTO "Attending_Event" VALUES('mike@example.com', 6, NULL);
INSERT INTO "Attending_Event" VALUES('mitch@example.com', 4, NULL);
INSERT INTO "Attending_Event" VALUES('mitch@example.com', 5, NULL);
INSERT INTO "Attending_Event" VALUES('mitch@example.com', 6, NULL);

INSERT INTO "Contact" VALUES(1, 'todd@example.com', '8144048227', 1);
INSERT INTO "Contact" VALUES(2, 'todd@example.com', 'todd@second.com', 0);
INSERT INTO "Contact" VALUES(3, 'mike@example.com', 'mike@second.com', 0);
INSERT INTO "Contact" VALUES(4, 'joel@example.com', '5551112222', 1);
INSERT INTO "Contact" VALUES(5, 'mitch@example.com', '5552223333', 1);

INSERT INTO "Notified_For" VALUES(1, 1, '1900-01-01 05:00:00')
INSERT INTO "Notified_For" VALUES(1, 2, '1900-01-01 12:00:00')
INSERT INTO "Notified_For" VALUES(1, 4, '1900-01-01 10:00:00')
INSERT INTO "Notified_For" VALUES(2, 1, '1900-01-01 04:00:00')
INSERT INTO "Notified_For" VALUES(2, 2, '1900-01-01 03:00:00')
INSERT INTO "Notified_For" VALUES(3, 1, '1900-01-01 05:00:00')
INSERT INTO "Notified_For" VALUES(3, 2, '1900-01-01 10:00:00')
INSERT INTO "Notified_For" VALUES(3, 3, '1900-01-01 12:00:00')
INSERT INTO "Notified_For" VALUES(3, 4, '1900-01-01 23:00:00')
INSERT INTO "Notified_For" VALUES(5, 3, '1900-01-01 07:00:00')
INSERT INTO "Notified_For" VALUES(5, 4, '1900-01-01 09:00:00')
