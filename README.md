# Doctor appointment management system

Our project is a web application that offers several features for patients and doctors. Patients can easily book appointments with doctors, view their blogs, and update their personal details. Doctors, on the other hand, can create dynamic blog posts and manage their personal information. Upon appointment confirmation, a calendar event is automatically created in the doctor's Google Calendar.

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

# Step 2 :

Go to the requirements.txt file location. Go to command prompt and run the following command to install the required packages.

pip install -r requirements.txt

# Step 3 :

In this project after a appointment confirmation calender event is created in doctor's google calender. If u want this feature
go to below link and create a account and then create a new project then get a calender api access credentials then paste it in the 
templates/users/ in the project folder. Otherwise Skip it and remove the code in the views.py in the users folder.

https://console.cloud.google.com/ 

# Step 4 :

Open a command prompt and go to manage.py location. run the below commands one by one.

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

copy the url like this shown in ur command prompt & paste in ur browser.

http://127.0.0.1:8000/

Now we successfully run a web application.


