INSERT INTO "Plays_For" VALUES('joel@example.com',1,3,'Handler',1);
INSERT INTO "Plays_For" VALUES('chris@example.com',1,20,'Cutter',NULL);
INSERT INTO "Plays_For" VALUES('todd@example.com',1,4,'Handler',NULL);
INSERT INTO "Plays_For" VALUES('mitch@example.com',2,10,'Defense',NULL);
INSERT INTO "Plays_For" VALUES('mike@example.com',2,14,'Striker',NULL);


INSERT INTO "Coaches" VALUES('joel@example.com',1);
INSERT INTO "Coaches" VALUES('mitch@example.com',2);

INSERT INTO "Team" VALUES(1,'Yak (TU Frisbee)');
INSERT INTO "Team" VALUES(2,'Trojan Lacrosse');

INSERT INTO "Event_Type" VALUES(1,'Game');
INSERT INTO "Event_Type" VALUES(2,'Practice');
INSERT INTO "Event_Type" VALUES(3,'Workout');
INSERT INTO "Event_Type" VALUES(4,'Team Bonding Event');

INSERT INTO "User" VALUES('joel@example.com','Joel Bierre','pass');
INSERT INTO "User" VALUES('chris@example.com','Chris Shelor','pass');
INSERT INTO "User" VALUES('todd@example.com','Todd Fenstermacher','pass');
INSERT INTO "User" VALUES('mitch@example.com','Mitch Pawlanta','pass');
INSERT INTO "User" VALUES('mike@example.com','Mike Kammes','pass');

INSERT INTO "Event" VALUES(1,'Away vs. IWU',1461988800000,'Matter Park',1,1);
INSERT INTO "Event" VALUES(2,'Tuesday practice',1462248000000,'Practice Field',1,2);
INSERT INTO "Event" VALUES(3,'End of year party',1463716800000,'Student Center',1,4);
INSERT INTO "Event" VALUES(4,'Home vs. Purdue',1461988800000,'Lacrosse Field',2,1);
INSERT INTO "Event" VALUES(5,'Walkthrough practice',1461902400000,'Practice Field',2,2);
INSERT INTO "Event" VALUES(6,'Thursday morning workout',1461816000000,'KSAC',2,3);
