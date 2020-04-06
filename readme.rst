Absenties
=========

Webapp from 2003 for registering school absentees.

Mainly here for showcasing.

It was meant for teachers to administer absentees from their classroom, and for others in the school to do so from their own workplace.

Built in Python using plain CGI and a little JavaScript.

For data it uses text files that are exported from the school's pupil tracking application. later I added a very crude system to support user login, at that time I used XML to store data.

for more info see https://www.magiokis.nl/docs/en/absenties/

Usage
-----

copy the contents of server-config-nginx or server-config-apache into your local webserver configuration and make it point to the right locations. Point your webbrowser to the specified domain.

Requirements
------------

- Python
- some test programs use `logbook <https://pypi.org/project/Logbook>`_ 
