# Tornado project 
### Author: Mohammad Hadi Hajihosseini

A RESTful api created using tornado.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

* python
* mysql
```
sudo apt install python mysql
```

## Requirement

You need to install these packages to run the server.py file.
* tornado
* hexlify (to generate random token)

```
pip install tornado hexlify
```

## Installing

### Step0 : Cloning

First of All Clone the Project : 
```
$ git clone https://github.com/hadiMh/tornado.git
$ cd tornado
```

### Step1 : Connect to MySQL and create a database

#### Connect to MySQL as a user that can create databases and users:
```
$ mysql -u root
```
Create a database named "ticketsapp":
```
mysql> CREATE DATABASE ticketsapp;
```
Allow the "myAadmin" user to connect with the password "myAdmin":
```
mysql> GRANT ALL PRIVILEGES ON myAadmin.* TO 'myAadmin'@'localhost' IDENTIFIED BY 'myAadmin';
```
Step2 : Create the tables in your new database

open the whole project file in the PyCharm IDE and connect the IDE to mysql database for this project.
Then create two tables in it, first the users table, and second the tickets table.

Then now you Must Put Database information in mydb.py from line 5 10

notice that I used an environmental variable to store the databese password. If you wanna publish your code or show it to some people it is better to make secret and sensitive information as env variables to make them secure.

Step3 : Run the ticketsapp project

With the default user, password, and database you can just run:
```
$ python server.py
```

I With you enjoy this code.
