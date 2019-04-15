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
import json
import collections



def createUserTicketList(userTicketList):
    result = {}
    if userTicketList:
        ticketListLength = len(userTicketList)
    else:
        ticketListLength = 0
    result[" tickets"] = "There Are -%d- Ticket" % ticketListLength
    result[" code"] = "200"

    i = 0
    if(userTicketList):
        for value in userTicketList:
            result["block %d" % i] = {
                "subject": value["subject"],
                "body": value["body"],
                "status": value["status"],
                "id": value["id"],
                "date": "2019-05-21 15:18:17",
                "response": value["response"]
            }
            i=i+1
    return result

def getQueryParametes(self, parameters):
    returnValues = []
    for value in parameters:
        result = re.search("(?<="+value+"=)([^&]+)?", self.request.uri)
        if(result):
            returnValues.append(result.group())
        else:
            returnValues.append(0)
    return returnValues

def getPostParameters(self, parameters):
    returnValues = []
    for value in parameters:
        result = self.get_argument(value)
        if(result):
            returnValues.append(result)
        else:
            returnValues.append(0)
    return returnValues



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


# request handler classes
class MyRequestHandler(RequestHandler):
    @property

    def hello(self):
        print("second function")


class SignupHandler(MyRequestHandler):
    def get(self, *args):
        username, password, firstname, lastname = getQueryParametes(self, ['username', 'password', 'firstname', 'lastname'])


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

            self.write({
                "message": "Signed Up Successfully",
                "code": "200"
            })
        else:
            self.write(
                {
                    "message": "user already exists",
                    "code": "400"
                }
            )

    def post(self, *args, **kwargs):
        username, password, firstname, lastname = getPostParameters(self,
                                                                    ['username', 'password', 'firstname', 'lastname'])


        if (not username or not password):
            self.write({
                "message:": "username and password are required",
                "code": "400"})
            return

        if (not firstname):
            firstname = ""

        if (not lastname):
            lastname = ""

        # check if user already exists in the saved users
        userExists = mydb.doesThisUserAlreadyExist(username)

        if not userExists:
            mydb.createUserInUsersTable(username, password, firstname, lastname)

            self.write({
                "message": "Signed Up Successfully",
                "code": "200"
            })
        else:
            self.write(
                {
                    "message": "user already exists",
                    "code": "300"
                }
            )

class LoginHandler(MyRequestHandler):
    def get(self, *args):
        # get username and password that the request contains
        username, password = getQueryParametes(self, ['username', 'password'])

        # if username or password are not in the request
        if(not username or not password):
            self.write({
                "message": "username and password are required.",
                "code": "400"
            })
            return

        # find the user if exist
        user = mydb.doesThisUserAlreadyExist(username)
        # if user doesnt exist, tell it to response
        if not user:
            self.write({
                "message": "user doesn't exist in the database.",
                "code": "400"
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
                "message": "username or password is not correct",
                "code": "400"
            })

    def post(self, *args, **kwargs):
        # get username and password that the request contains
        username, password = getPostParameters(self, ['username', 'password'])
        # username = self.get_argument('username')
        # password = self.get_argument('password')
        print("post parameters", username, password)
        # if username or password are not in the request
        if (not username or not password):
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
        username, password = getQueryParametes(self, ['username', 'password'])
        if (not username or not password):
            self.write({
                "message": "username and password are required."
            })
            return
        # find the user if exist
        user = mydb.clearUserToken(username, password)
        # if user doesnt exist, tell it to response
        if not user:
            self.write({
                "message": "user have already logged out or "
                           "user doesn't exist in the database or "
                           "your password is not correct"
            })
            return

        # if user exist and the password is correct
        if (user):
            # clear the token so the user is logged out
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

    def post(self, *args, **kwargs):
        username, password = getPostParameters(self, ['username', 'password'])
        if (not username or not password):
            self.write({
                "message": "username and password are required."
            })
            return
        # find the user if exist
        user = mydb.clearUserToken(username, password)
        # if user doesnt exist, tell it to response
        if not user:
            self.write({
                "message": "user have already logged out or "
                           "user doesn't exist in the database or "
                           "your password is not correct"
            })
            return

        # if user exist and the password is correct
        if (user):
            # clear the token so the user is logged out
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

        user = mydb.getUserByToken(token)

        if(not user):
            self.write({
                "message": "token not valid"
            })
            return

        ticketId = mydb.saveTicket(user['username'], subject, body)

        self.write({
             "message": "Ticket Sent Successfully",
             "id": ticketId,
             "code": "200"
        })

    def post(self, *args, **kwargs):
        token, subject, body = getPostParameters(self, ['token', 'subject', 'body'])
        if (not token):
            self.write({
                "message": "token is required. please login first."
            })
            return
        if (not subject or not body):
            self.write({
                "message": "subject and body of the ticket are required."
            })
            return

        user = mydb.getUserByToken(token)

        if (not user):
            self.write({
                "message": "token not valid"
            })
            return

        ticketId = mydb.saveTicket(user['username'], subject, body)

        self.write({
            "message": "Ticket Sent Successfully",
            "id": ticketId,
            "code": "200"
        })

class UserGetTicketHandler(MyRequestHandler):
    def get(self, *args):
        token = getQueryParametes(self, ['token'])[0]
        if(not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = mydb.getUserByToken(token)

        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = mydb.getAllUserTickets(user['username'])
        if userTickets:
            numberOfTickets = len(userTickets)
        else:
            numberOfTickets = 0
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            collections.OrderedDict(sorted(correctFormatUserTicketsList.items()))
        )

    def post(self, *args):
        token = getPostParameters(self, ['token'])[0]
        if(not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = mydb.getUserByToken(token)

        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = mydb.getAllUserTickets(user['username'])

        numberOfTickets = len(userTickets)
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            collections.OrderedDict(sorted(correctFormatUserTicketsList.items()))
        )

class UserCloseTicketHandler(MyRequestHandler):
    def get(self, *args):
        token, id = getQueryParametes(self, ['token', 'id'])
        user = mydb.getUserByToken(token)
        userTickets = mydb.getAllUserTickets(user["username"])
        if mydb.doesThisTicketExists(id) and mydb.changeTicketStatus(id, "Closed"):
            self.write({
                "message": "Ticket With id -%s- Closed Successfully" % id,
                "code": "200"
            })
            return
        else:
            self.write({
                "message": "No such user or ticket",
                "code": "404"
            })
            return

    def post(self, *args, **kwargs):
        token, id = getPostParameters(self, ['token', 'id'])
        user = mydb.getUserByToken(token)
        userTickets = mydb.getAllUserTickets(user["username"])
        if(mydb.changeTicketStatus(id, "Closed")):
            self.write({
                "message": "Ticket With id -%s- Closed Successfully" % id,
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
        token, = getQueryParametes(self, ['token'])
        if (not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = mydb.getUserByToken(token)
        print("isthisuseradmin",mydb.isThisTokenAdmin(token))
        if not user or not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = mydb.getAllUserTickets(user["username"])
        numberOfTickets = len(userTickets)
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            collections.OrderedDict(sorted(correctFormatUserTicketsList.items()))
        )

    def post(self, *args, **kwargs):
        token, = getPostParameters(self, ['token'])
        if (not token):
            self.write({
                "message": "request in correct format"
            })
            return

        user = mydb.getUserByToken(token)
        print("isthisuseradmin",mydb.isThisTokenAdmin(token))
        if not user or not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        userTickets = mydb.getAllUserTickets(user["username"])
        numberOfTickets = len(userTickets)
        correctFormatUserTicketsList = createUserTicketList(userTickets)

        self.write(
            collections.OrderedDict(sorted(correctFormatUserTicketsList.items()))
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

        user = mydb.getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        if mydb.doesThisTicketExists(id) and mydb.saveThisResponseForThisTicket(id, body):
            self.write({
                "message": "Response to Ticket With id -%s- Sent Successfully" % id,
                "code": "200"
            })
        else:
            self.write({
                "message": "Response to Ticket With id -%s- Was not Successfully. Please get sure for ticket existence." % id,
                "code": "200"
            })

    def post(self, *args, **kwargs):
        token, id, body = getPostParameters(self, ['token', 'id', 'body'])
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

        user = mydb.getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        if mydb.doesThisTicketExists(id) and mydb.saveThisResponseForThisTicket(id, body):
            self.write({
                "message": "Response to Ticket With id -%s- Sent Successfully" % id,
                "code": "200"
            })
        else:
            self.write({
                "message": "Response to Ticket With id -%s- Was not Successfully. Please get sure for ticket existence." % id,
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

        user = mydb.getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        if  mydb.doesThisTicketExists(id) and mydb.changeTicketStatus(id, status):
            self.write({
                "message": "Status Ticket With id -%s- Changed Successfully" % id,
                "code": "200"
            })
            return
        else:
            self.write({
                "message": "No such ticket or user",
                "code": "404"
            })
            return

    def post(self, *args, **kwargs):
        token, id, status = getPostParameters(self, ['token', 'id', 'status'])
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

        user = mydb.getUserByToken(token)
        if not user:
            self.write({
                "message": "token is not valid"
            })
            return

        if not mydb.isThisTokenAdmin(token):
            self.write({
                "message": "token is not valid"
            })
            return

        if  mydb.doesThisTicketExists(id) and mydb.changeTicketStatus(id, status):
            self.write({
                "message": "Status Ticket With id -%s- Changed Successfully" % id,
                "code": "200"
            })
            return
        else:
            self.write({
                "message": "No such ticket or user",
                "code": "404"
            })
            return

class DefaultHandler(MyRequestHandler):
    def get(self, *args):
        self.write({
            "message": "page does not exist"
        })
        print(self.request)

def make_app():
    urls = [
        # GET Urls
        (r"/signup(.*)", SignupHandler),
        (r"/login(.*)", LoginHandler),
        (r"/logout(.*)", LogoutHandler),
        (r"/sendticket(.*)", SendTicketHandler),
        (r"/getticketcli(.*)", UserGetTicketHandler),
        (r"/closeticket(.*)", UserCloseTicketHandler),
        (r"/getticketmod(.*)", AdminGetAllTicketsHandler),
        (r"/restoticketmod(.*)", AdminAnswerToTicketHandler),
        (r"/changestatus(.*)", AdminChangeTicketStatus),

        # POST Urls
        (r"/signup", SignupHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/sendticket", SendTicketHandler),
        (r"/getticketcli", UserGetTicketHandler),
        (r"/closeticket", UserCloseTicketHandler),
        (r"/getticketmod", AdminGetAllTicketsHandler),
        (r"/restoticketmod", AdminAnswerToTicketHandler),
        (r"/changestatus", AdminChangeTicketStatus),

        (r".*", DefaultHandler)
    ]
    return Application(urls)

app = make_app()
app.listen(3000)
# print(options['mysql-database'])
IOLoop.instance().start()