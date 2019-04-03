import mysql.connector
import os
from time import gmtime, strftime

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

def getUserByToken(token):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM users WHERE token = %s"
    value = (token, )

    mycursor.execute(sql, value)

    myresult = mycursor.fetchall()

    if (mycursor.rowcount >= 1):
        return {
            "username": myresult[0][1],
            "password": myresult[0][2],
            "firstname": myresult[0][3],
            "lastanme": myresult[0][4],
            "token": myresult[0][5],
            "isAdmin": myresult[0][6]
        }
    return 0

def saveTicket(username, subject, body):
    mycursor = mydb.cursor()

    sql = "INSERT INTO tickets (username, subject, body, status, date) VALUES (%s, %s, %s, 'open', %s)"
    val = (username, subject, body, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted to tickets table.")

    return mycursor.lastrowid

def getAllUserTickets(username):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM tickets WHERE username = %s"
    value = (username, )

    mycursor.execute(sql, value)

    myresult = mycursor.fetchall()

    json = []

    if (mycursor.rowcount >= 1):
        for item in myresult:
            json.append({
                "id": item[0],
                "username": item[1],
                "subject": item[2],
                "body": item[3],
                "status": item[4],
                "date": item[5],
                "response": item[6] or ''
            })
        return json

    return 0

def clearUserToken(username, password):
    mycursor = mydb.cursor()

    sql = "SELECT * FROM users WHERE username = %s"
    value = (username,)

    mycursor.execute(sql, value)

    myresult = mycursor.fetchall()
    user = 0
    if mycursor.rowcount >= 1:
        user = {
            "username": myresult[0][1],
            "password": myresult[0][2],
            "firstname": myresult[0][3],
            "lastanme": myresult[0][4],
            "token": myresult[0][5]
        }
    if(user == 0):
        return 0

    if password != user['password']:
        return 0

    mycursor = mydb.cursor()

    sql = "UPDATE users SET token = %s WHERE username = %s"
    value = ('', username)

    mycursor.execute(sql, value)

    mydb.commit()

    if (mycursor.rowcount >= 1):
        print("logout was successful for %s" % username)
    else:
        return 0

    return 1

def changeTicketStatus(ticketId, newStatus):
    mycursor = mydb.cursor()

    sql = "UPDATE tickets SET status = %s WHERE id = %s"
    value = (newStatus, ticketId)

    mycursor.execute(sql, value)

    mydb.commit()

    print("ticket id=%s was changed status to %s" % (ticketId, newStatus))

    return 1

def isThisTokenAdmin(token):
    user = getUserByToken(token)
    if not user:
        return 0
    if user['isAdmin'] == 1:
        return True
    return False

def saveThisResponseForThisTicket(id, body):
    mycursor = mydb.cursor()

    sql = "UPDATE tickets SET response = %s, status = %s WHERE id = %s"
    value = (body, 'Closed', id)

    mycursor.execute(sql, value)

    mydb.commit()

    print("ticket id=%s was set response to %s" % (id, body))

    return 1
