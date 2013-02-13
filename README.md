CATEScraper
===========

An API that scrapes Imperial College's DoC web platform to process the data on project hand-ins.
Run the Parser.py script with arguments in this order...
    login, password, class, period

Period is in the format {(1,AUTUMN),(3,SPRING),(5,SUMMER)}
Class is something like 'c1'

Updated to include the bottle package that allows RESTful api access.
The Parser.py script now creates a local python server which when
accessed at http://localhost:8080/<login>/<password>/<class>/<period>
will return a csv file containing the information for both modules and
exercises.

The csv files are formatted like so - any values are enclosed in double
quotation marks and any tuples are therefore formatted like so:
  
  (A,B) will become literally ("A","B")

The two tables (modules and exercises) are separated by three br
markers. Each entry is delimited by a single br
