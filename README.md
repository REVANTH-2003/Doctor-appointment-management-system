# Doctor appointment management system

Automated Weather Classification system that utilizes Transfer Learning techniques. The aim of this project was to develop an efficient and accurate system for classifying weather conditions based on images.

# Steps to run a application :

# Step 1 :

Download & Install a python 3.10 or later versions using a below link and set a environment variables.

https://www.python.org/downloads/

In this project we use a default database sqlite we also use a Mysql database. If u want then Do the Database activity steps othervise
Don't do the database related steps.

# Database related steps:

1. Download a mysql and install it. follow the guidelines in a youtube link
https://youtu.be/eq-e_n7lm2M

2. Go to command prompt and run the following commands one by one.
pip install mysql-connector-python
pip install mysqlclient

3. Open a mysql and run the below command for create a database.
create database appointmentmanagement;

4. Go to appointment_management folder and open a settings.py file.

Change a user name and password in the database to your username and password of mysql.

DATABASES = {

'default': {

'ENGINE': 'django.db.backends.mysql',

'NAME': 'appointment-management',

'USER':'root', ----> replace with ur username

'PASSWORD':'root', ----> replace with your password 
} }


# Step 4 :

Open a command prompt and go to manage.py location. run the below commands one by one.

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

copy the url like this shown in ur command prompt & paste in ur browser.

http://127.0.0.1:8000/

Now we successfully run a web application.


