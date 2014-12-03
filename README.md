anony-course-feedback
=====================

A course feedback portal with a special emphasis on anonymity and security. It also features a unique anonymous chat where students can chat anonymously and privately with their professors. Here anonymity is maintained, but students can still edit their previous feedback. See the pdf enclosed for more details.

Development Status
====================
We beleive that this is very close to being completely deployable, but some work on the encryption side is recommended so that even if the website security is compromised (which should not be very easy, we hope), the data is reasonable secure.

Running the Server
==================
This is based on a python-django server model. To run the development server navigate in the command line to the relevant directory and type "python manage.py runserver". Then, in your browser, type "localhost:8000/feedback" and the login page should open. The database will be a basic sample database. To create your own database read the section below. 

To know the basic data in the database stored now, see populateDatabse.py or navigate to "localhost:8000/admin". Login with "username: admin, password:admin" and go to "User" to view the usernames. The password is "passy" for the professor accounts and "spassy" for the student accounts.

The Database
============
First delete the sample database given ("db.sqlite3") and do "python manage.py syncdb". Now go to "populateDatabase.py" and modify it according to your needs. The script below will call the relevant functions to populate the databse. The portal should be ready to use now.

Requirements
============
Python:
  Python v2.7
  Django
  Nltk
