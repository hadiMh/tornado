import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="hadimh",
    passwd=os.environ['DBPASSWORD'],
    database= 'tickets'
)

def createUserInUsersTable(username, password, firstname, lastname):
    mycursor = mydb.cursor()

    if(not firstname):
        firstname = ''
    if(not lastname):
        lastname = ''

    sql = "INSERT INTO users (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)"
    val = (username, password, firstname, lastname)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def printAllUsers():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

def doesThisUserAlreadyExist(username):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM users WHERE username = %s"
    value = (username, )

    mycursor.execute(sql, value)

    myresult = mycursor.fetchall()

    if len(myresult) >= 1:
        return {
            "username": myresult[0][1],
            "password": myresult[0][2],
            "firstname": myresult[0][3],
            "lastanme": myresult[0][4],
            "token": myresult[0][5]
        }
    return False

def saveTokenToThisUser(username, token):
    mycursor = mydb.cursor()

    sql = "UPDATE users SET token = %s WHERE username = %s"
    value = (token, username)

    mycursor.execute(sql, value)

    mydb.commit()

    if(mycursor.rowcount >= 1):
        print("saving token was successful")

