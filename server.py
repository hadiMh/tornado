import re
import os
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
import string
import random
# from torndb import Connection
from binascii import hexlify
from time import gmtime, strftime
import mydb

define("port", default=3000, help="run on the given port", type=int)
define("mysql_host", default="localhost:3306", help="database host")
define("mysql_database", default="tornadoapp1", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="", help="database password")
#
# myDbConnection = Connection(
#             host=options.mysql_host, database=options.mysql_database,
#             user=options.mysql_user, password=options.mysql_password
#             )
#
# print(options.mysql_database)

admins = [
    {
        "username": "hadi"
    }
]

users = [
    {
        "username": "hadi",
        "password": "1234",
        "firstname": "hadi",
        "lastname": "",
        "token": ""
    }
]

tickets = []

def createUserTicketList(userTicketList):
    result = {}

    result["tickets"] = "There Are -%d- Ticket" % len(userTicketList)
    result["code"] = "200"

    for idx, value in enumerate(userTicketList):
        result["block %d" % idx] = {
            "subject": value["subject"],
            "body": value["body"],
            "status": value["status"],
            "id": value["id"],
            "date": "2019-05-21 15:18:17",
            "response": value["response"]
        }
    return result

def getTicketId():
    if(not tickets):
        return 1
    return tickets[len(tickets)-1]["id"]+1

def getQueryParametes(self, parameters):
    returnValues = []
    for value in parameters:
        result = re.search("(?<="+value+"=)([^&]+)?", self.request.uri)
        if(result):
            returnValues.append(result.group())
        else:
            returnValues.append(0)
    return returnValues

def getUserByToken(token):
    for item in users:
        if(item["token"] == token):
            return item
    return 0

# global methods
def findUser(username):
    for user in users:
        print("user['username']:", user["username"])
        print("username:", username)
        if(user["username"] == username):
            return user
    return -1

def generateRandomToken():
    return hexlify(os.urandom(16)).decode('utf-8')

def getUserLoginToken(username):
    user = mydb.doesThisUserAlreadyExist(username)
    if(not user):
        print("no such user exists for login")
    else:
        if(not user["token"] or user["token"] == ""):
            user['token'] = generateRandomToken()
            mydb.saveTokenToThisUser(username, user['token'])
        return user['token']

def changeTicketStatus(tickets, ticketId, newStatus):
    for item in tickets:
        if '%d'%item["id"] == ticketId:
            item["status"] = newStatus
            return 1
    return 0

def isThisUsernameAdmin(username):
    for admin in admins:
        if(admin["username"] == username):
            return True
    return False

def getUserAllTickets(username):
    userAllTickets = []
    admin = False
    if isThisUsernameAdmin(username):
        admin = True
    for item in tickets:
        if admin or item["username"] == username:
            userAllTickets.append(item)

    return userAllTickets

def saveThisResponseForThisTicket(ticketId, body):
    for item in tickets:
        if '%d'%item["id"] == ticketId:
            item["response"] = body
            item["status"] = "Closed"
            return True
    return False

# request handler classes
class MyRequestHandler(RequestHandler):
    @property

    def ifUserAlreadyExists(self, username):
        for item in users:
            if(item["username"] and item["username"] == username):
                return True
        return False

    def hello(self):
        print("second function")

# class LoginHandler(MyRequestHandler):
#     def get(self, *args):
#         users.append({"username": args[0], "password": args[1]})
#         # print(users)
#         self.write({'message': users})

class SignupHandler(MyRequestHandler):
    def get(self, *args):
        username, password, firstname, lastname = getQueryParametes(self, ['username', 'password', 'firstname', 'lastname'])
        ## username = re.search("(?<=username=)([^&]+)?", self.request.uri)
        ## password = re.search("(?<=password=)([^&]+)?", self.request.uri)
        ## firstname = re.search("(?<=firstname=)([^&]+)?", self.request.uri)
        ## lastname = re.search("(?<=lastname=)([^&]+)?", self.request.uri)

        if(not username or not password):
            self.write({"message:": "username and password are required"})
            return

        if(not firstname):
            firstname = ""

        if(not lastname):
            lastname = ""

        # check if user already exists in the saved users
        userExists = mydb.doesThisUserAlreadyExist(username)

        if not userExists:
            mydb.createUserInUsersTable(username, password, firstname, lastname)
            users.append(
                {
                    "username": username,
                    "password": password,
                    "firstname": firstname,
                    "lastname": lastname,
                    "token": ""
                }
            )
            self.write({
                "message": "Signed Up Successfully",
                "code": "200"
            })
        else:
            self.write("user already exists")

class LoginHandler(MyRequestHandler):
    def get(self, *args):
        # get username and password that the request contains
        username, password = getQueryParametes(self, ['username', 'password'])

        # if username or password are not in the request
        if(not username or not password):
            self.write({
                "message": "username and password are required."
            })
            return

        # find the user if exist
        user = mydb.doesThisUserAlreadyExist(username)
        # if user doesnt exist, tell it to response
        if not user:
            self.write({
                "message": "user doesn't exist in the database."
            })
            return
        print("user", user)
        # if user exist and the password is correct
        if (user) and user["password"] == password:
            # the below function, saves the token in the user data
            token = getUserLoginToken(username=username)
            self.write({
                "message": "Logged in Successfully",
                "code": "200",
                "token": token
            })
        else:
            # if the password is not correct
            self.write({
                "message": "username or password is not correct"
            })

class LogoutHandler(MyRequestHandler):
    def get(self, *args):
        username = re.search("(?<=username=)([^&]+)?", self.request.uri)
        password = re.search("(?<=password=)([^&]+)?", self.request.uri)
        if (not username or not password):
            self.write({
                "message": "username and password are required."
            })
            return
        # find the user if exist
        user = findUser(username.group())
        # if user doesnt exist, tell it to response
        if user == -1:
            self.write({
                "message": "user doesn't exist in the database."
            })
            return

        # if user exist and the password is correct
        if (user != -1) and user["password"] == password.group():
            # clear the token so the user is logged out
            user["token"] = ""
            self.write({
                "message": "Logged Out Successfully",
                "code": "200"
            })
            return
        else:
            # if the password is not correct
            self.write({
                "message": "username or password is not correct"
            })

class SendTicketHandler(MyRequestHandler):
    def get(self, *args):
        token, subject, body = getQueryParametes(self, ['token', 'subject', 'body'])
        if(not token):
            self.write({
                "message": "token is required. please login first."
            })
            return
        if(not subject or not body):
            self.write({
                "message": "subject and body of the ticket are required."
            })
            return
        user = getUserByToken(token)
        if(not user):
            self.write({
                "message": "token not valid"
            })
            return

        id = getTicketId()

        tickets.append({
            "username": user["username"],
            "subject": subject,
            "body": body,
            "id": id,
            "date": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "status": "Open",
            "response": ""
        })
        self.write({
             "message": "Ticket Sent Successfully",
             "id": id,
             "code": "200"
        })

class GetAllTicketsHandler(MyRequestHandler):
    def get(self, *args):
        print(tickets)

class UserGetTicketHandler(MyRequestHandler):
    def get(self, *args):
        token = getQueryParametes(self, ['token'])[0]
        if(not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = getUserByToken(token)

        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = getUserAllTickets(user["username"])
        numberOfTickets = len(userTickets)
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            correctFormatUserTicketsList
        )

class UserCloseTicketHandler(MyRequestHandler):
    def get(self, *args):
        token, id = getQueryParametes(self, ['token', 'id'])
        user = getUserByToken(token)
        userTickets = getUserAllTickets(user["username"])
        if(changeTicketStatus(userTickets, id, "Closed")):
            self.write({
                "message": "Ticket With id -%d- Closed Successfully" % id,
                "code": "200"
            })
            return
        else:
            self.write({
                "message": "No such user or ticket",
                "code": "404"
            })
            return

class AdminGetAllTicketsHandler(MyRequestHandler):
    def get(self, *args):
        token = getQueryParametes(self, ['token'])[0]
        if (not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = getUserByToken(token)

        if not user or not isThisUsernameAdmin(user["username"]):
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = getUserAllTickets(user["username"])
        numberOfTickets = len(userTickets)
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            correctFormatUserTicketsList
        )

class AdminAnswerToTicketHandler(MyRequestHandler):
    def get(self, *args):
        token, id, body = getQueryParametes(self, ['token', 'id', 'body'])
        if(not token):
            self.write({
                "message": "token is required"
            })
            return
        if(not id or not body):
            self.write({
                "message": "the ticket id and the response text are required"
            })
            return

        user = getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not isThisUsernameAdmin(user["username"]):
            self.write({
                "message": "token is not valid"
            })
            return

        if saveThisResponseForThisTicket(id, body):
            self.write({
                "message": "Response to Ticket With id -%s- Sent Successfully" % id,
                "code": "200"
            })
        else:
            self.write({
                "message": "Response to Ticket With id -%s- Was not Successfully" % id,
                "code": "200"
            })

class AdminChangeTicketStatus(MyRequestHandler):
    def get(self, *args):
        token, id, status = getQueryParametes(self, ['token', 'id', 'status'])
        if (not token):
            self.write({
                "message": "token is required"
            })
            return
        if (not id or not status):
            self.write({
                "message": "the ticket id and the status are required"
            })
            return

        user = getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not isThisUsernameAdmin(user["username"]):
            self.write({
                "message": "token is not valid"
            })
            return

        if (changeTicketStatus(tickets, id, status)):
            self.write({
                "message": "Status Ticket With id -%s- Changed Successfully" % id,
                "code": "200"
            })
            return
        else:
            self.write({
                "message": "No such user or ticket",
                "code": "404"
            })
            return


class DefaultHandler(MyRequestHandler):
    def get(self, *args):
        self.write("default handler")
        print(self.request)

def make_app():
    urls = [
        # ("/", HelloHandler),
        # (r"/hadi/([^/]+)?", SecondHandler)
        (r"/login/([^/]+)?/([^/]+)?", LoginHandler),
        (r"/signup(.*)", SignupHandler),
        (r"/login(.*)", LoginHandler),
        (r"/logout(.*)", LogoutHandler),
        (r"/sendticket(.*)", SendTicketHandler),
        (r"/gettickets", GetAllTicketsHandler),
        (r"/getticketcli(.*)", UserGetTicketHandler),
        (r"/closeTicket(.*)", UserCloseTicketHandler),
        (r"/getticketmod(.*)", AdminGetAllTicketsHandler),
        (r"/restoticketmod(.*)", AdminAnswerToTicketHandler),
        (r"/changestatus(.*)", AdminChangeTicketStatus),
        (r".*", DefaultHandler)
    ]
    return Application(urls)

app = make_app()
app.listen(3000)
# print(options['mysql-database'])
IOLoop.instance().start()