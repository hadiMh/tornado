import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="hadimh",
    passwd="mhdh1999",
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
        return True
    return False