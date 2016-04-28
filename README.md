# Team Manager
Project for Database class

## Dependencies 
1. Python 2.7 or Python 3.5
2. Sqlite3

## How to use
* Create a db.sqlite file in the root directory of the project
    * `$ touch db.sqlite` for a unix based machine
* Run the createdb.sql commands to create the schema of the database
    * `$ sqlite3 db.sqlite < createdb.sql` 
* Run the insertvalues.sql commands to populate database
    * `$ sqlite3 db.sqlite < insertvalues.sql`
* Run `$ python team-manage.py`from command line
* Go to 127.0.0.1:5000 
* All links are working 

Disclaimer:
We did not have time to implement a login (as this wasn't a top priority for a database project)
So... On the events page if you want to see an individual's events for his sport then 
you must add his email to the end of the url. I give an example on the events page itself. 
