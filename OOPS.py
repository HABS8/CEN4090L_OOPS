import os
from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3
import encryption
import pandas as pd
import socket
import sys
import hmac, hashlib


app = Flask(__name__)

######### functions for the website goo here ########

def home():
    if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
        return render_template('Login.html')
    else:
        return render_template('Home.html', name=session['name'])

######################################################

# main function that renders the website
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)



    



########################################################
# for reference #

# # renders the home page of website function that renders 'Home.html'
# # if user is longed in else takes user to the login page
# @app.route('/')
# def home():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
#         return render_template('Login.html')
#     else:
#         return render_template('Home.html', name=session['name'])


# # add a new Auction Bidder page of website function that renders 'Add_a_new_Auction_Bidder.html'
# # if the user has app role level 1
# @app.route('/Add_a_new_Auction_Bidder')
# def add_bidder():
#     if not session.get('logged_in1'):
#         # if the user has app role leve 2 or 3
#         # it displays "page not found" to the user in the "Results.html" page
#         if session.get('logged_in2') or session.get('logged_in3'):
#             msg = "page not found"
#             return render_template("Results.html", msg=msg)
#         # else takes user to the login page
#         else:
#             return render_template('Login.html')
#     else:
#         return render_template('Add_a_new_Auction_Bidder.html')


# # the function extract the bidder information from
# # what the user submit in the 'Add_a_new_Auction_Bidder.html' page
# # if the user has app role level 1
# @app.route('/addrec', methods=['POST', 'GET'])
# def addrec():
#     if not session.get('logged_in1'):
#         # if the user has app role leve 2 or 3
#         # it displays "page not found" to the user in the "Results.html" page
#         if session.get('logged_in2') or session.get('logged_in3'):
#             msg = "page not found"
#             return render_template("Results.html", msg=msg)
#         # else takes user to the login page
#         else:
#             return render_template('Login.html')
#     else:
#         if request.method == 'POST':

#             # extracts the bidder name and checks if the string is not empty
#             # or only contains spaces
#             # if this condition is met nameB is set to true and an error message is initialized
#             # else it is set to false
#             name = request.form['name']
#             if (len(name) == 0) or name.isspace():
#                 nameB = False
#                 msg_Name = "You can not enter in an empty name"
#                 msg = ""
#             else:
#                 msg_Name = ""
#                 nameB = True

#             # extracts the bidder phone number and checks if the string is not empty
#             # or only contains spaces
#             # if this condition is met phone_numberB is set to true and an error message is initialized
#             # else it is set to false
#             phone_number = request.form['Phone Number']
#             if (len(phone_number) == 0) or phone_number.isspace():
#                 phone_numberB = False
#                 msg_phone_number = "You can not enter in an empty phone number"
#                 msg = ""
#             else:
#                 msg_phone_number = ""
#                 phone_numberB = True

#             # extracts the bidder Prequalified Upper Limit and checks if its numeric
#             # or is greater than zero
#             # if this condition is met pulB is set to true and an error message is initialized
#             # else it is set to false
#             pul = request.form['Prequalified Upper Limit']
#             if (not str(pul).isnumeric()) or (int(pul) <= 0):
#                 pulB = False
#                 msg_pul = "The Prequalified Upper Limit must be a numeric greater than 0"
#                 msg = ""
#             else:
#                 msg_pul = ""
#                 pulB = True

#             # extracts the bidder App Role Level and checks if its numeric
#             # or is a number between 1 and 3 inclusive
#             # if this condition is met arlB is set to true and an error message is initialized
#             # else it is set to false
#             arl = request.form['App Role Level']
#             if (not str(arl).isnumeric()) or (1 > int(arl)) or (int(arl) > 3):
#                 arlB = False
#                 msg_arl = "The AppRoleLevel must be a numeric between 1 and 3"
#                 msg = ""
#             else:
#                 msg_arl = ""
#                 arlB = True

#             # extracts the bidder Login Password and checks if the string is not empty
#             # or only contains spaces
#             # if this condition is met pwdB is set to true and an error message is initialized
#             # else it is set to false
#             pwd = request.form['Login Password']
#             if (len(pwd) == 0) or pwd.isspace():
#                 pwdB = False
#                 msg_pwd = "You can not enter in an empty pwd"
#                 msg = ""
#             else:
#                 msg_pwd = ""
#                 pwdB = True

#             con = sqlite3.connect('BidderDB.db')
#             # if all conditions were met it inserts the bidder information into the database 'BidderDB.db'
#             if nameB and phone_numberB and pulB and arlB and pwdB:

#                 # encrypts the name, phone number, and password before inserting them into the database
#                 name = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
#                 phone_number = str(Encryption.cipher.encrypt(bytes(phone_number, 'utf-8')).decode("utf-8"))
#                 pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

#                 cur = con.cursor()
#                 cur.execute("INSERT INTO Bidder (BidderName, PhoneNumber, PrequalifiedUpperLimit, "
#                             "AppRoleLevel, LoginPassword) VALUES (?, ?, ?, ?, ?)",
#                             (str(name), str(phone_number), int(pul), int(arl), str(pwd)))
#                 msg = "Record successfully added"
#                 con.commit()
#             # else rolls back
#             else:
#                 con.rollback()
#             con.close()

#             # displays if the task was successful else display the errors in "Results.html" page
#             return render_template("Results.html", msg=msg, msg_Name=msg_Name, msg_phone_number=msg_phone_number,
#                                    msg_pul=msg_pul, msg_arl=msg_arl, msg_pwd=msg_pwd)


# # List Auction Bidders of website function that renders "List_Auction_Bidders.html"
# # renders all the bidders information
# # if the user has app role level 1 or 2
# @app.route('/List_Auction_Bidders')
# def display_bidder_data():
#     if not session.get('logged_in1') and not session.get('logged_in2'):
#         # if the user has app role leve 3
#         # it displays "page not found" to the user in the "Results.html" page
#         if session.get('logged_in3'):
#             msg = "page not found"
#             return render_template("Results.html", msg=msg)
#         # else takes user to the login page
#         else:
#             return render_template('Login.html')
#     else:
#         con = sqlite3.connect('BidderDB.db')
#         con.row_factory = sqlite3.Row

#         cur = con.cursor()
#         cur.execute("SELECT BidderName, PhoneNumber, PrequalifiedUpperLimit, AppRoleLevel, LoginPassword FROM Bidder")

#         df = pd.DataFrame(cur.fetchall(), columns=['BidderName', 'PhoneNumber',
#                                                    'PrequalifiedUpperLimit', 'AppRoleLevel',
#                                                    'LoginPassword'])

#         # decrypts the 'BidderName' before displaying it to the user
#         index = 0
#         for nm in df['BidderName']:
#             nm = str(Encryption.cipher.decrypt(nm))
#             df._set_value(index, 'BidderName', nm)
#             index += 1

#         # decrypts the 'PhoneNumber' before displaying it to the user
#         index = 0
#         for nm in df['PhoneNumber']:
#             nm = str(Encryption.cipher.decrypt(nm))
#             df._set_value(index, 'PhoneNumber', nm)
#             index += 1

#         con.close()

#         return render_template("List_Auction_Bidders.html", rows=df)


# # extracts the username and password from
# # what the user submits in the 'Login.html' page
# @app.route('/Login', methods=['POST'])
# def do_admin_login():
#     try:
#         # sets the session name to an empty string
#         # and logs out the user out of any app level
#         session['name'] = ""
#         session['BidderID'] = ""
#         session['logged_in1'] = False
#         session['logged_in2'] = False
#         session['logged_in3'] = False

#         name = request.form['username']
#         pwd = request.form['password']

#         # encrypts the name and password before checking there existence in the database
#         name = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
#         pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

#         # validates the username and password from the database
#         with sqlite3.connect('BidderDB.db') as con:
#             con.row_factory = sqlite3.Row
#             cur = con.cursor()

#             sql_select_query = """SELECT * FROM Bidder WHERE BidderName = ? and LoginPassword = ?"""
#             cur.execute(sql_select_query, (name, pwd))

#             row = cur.fetchone()

#             # if the name and password are valid
#             # sets the session name to name
#             if row is not None:

#                 # decrypts the name that will be displayed in the home page
#                 session['name'] = str(Encryption.cipher.decrypt(name))

#                 # requests the app role level of the user from the database
#                 roll_query = """SELECT BidderId FROM Bidder WHERE BidderName = ? and LoginPassword = ?"""
#                 cur.execute(roll_query, (name, pwd))
#                 session['BidderID'] = cur.fetchone()[0]

#                 # requests the app role level of the user from the database
#                 roll_query = """SELECT AppRoleLevel FROM Bidder WHERE BidderName = ? and LoginPassword = ?"""
#                 cur.execute(roll_query, (name, pwd))
#                 roll = cur.fetchone()[0]

#                 # depending on the roll level
#                 # it gives accesses to user
#                 # by setting the boolean assisted
#                 # with the roll level to true
#                 # and the rest to false
#                 if roll == 1:
#                     session['logged_in1'] = True
#                     session['logged_in2'] = False
#                     session['logged_in3'] = False
#                 elif roll == 2:
#                     session['logged_in1'] = False
#                     session['logged_in2'] = True
#                     session['logged_in3'] = False
#                 elif roll == 3:
#                     session['logged_in1'] = False
#                     session['logged_in2'] = False
#                     session['logged_in3'] = True
#             # else sets the session name to an empty string
#             # and logs out the user out of any app level
#             # and displays 'invalid username and/or password!'
#             else:
#                 session['name'] = ""
#                 session['BidderID'] = ""
#                 session['logged_in1'] = False
#                 session['logged_in2'] = False
#                 session['logged_in3'] = False
#                 flash('invalid username and/or password!')
#     except:
#         # in case of failure the database rolls back and
#         #  displays "error in insert operation"
#         con.rollback()
#         flash("error in insert operation")
#     finally:
#         # closes the connection to the 'BidderDB.db' database
#         con.close()
#     return home()


# # logout rout that sets the session name to an empty string
# # and makes all the logins to False
# # then returns the home function
# @app.route("/logout")
# def logout():
#     session['name'] = ""
#     session['BidderID'] = ""
#     session['logged_in1'] = False
#     session['logged_in2'] = False
#     session['logged_in3'] = False
#     return home()


# # List Auction Items of website function that renders "List_Auction_Items.html"
# # renders all the item information
# # if the user has app role level 1, 2 or 3
# @app.route('/List_Auction_Items')
# def display_items_data():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):

#         # else takes user to the login page
#         return render_template('Login.html')

#     else:
#         con = sqlite3.connect('AuctionItemDB.db')
#         con.row_factory = sqlite3.Row

#         cur = con.cursor()
#         cur.execute("SELECT ItemName, ItemDescription, LowestBidLimit, HighestBidderAmount FROM AuctionItem")

#         df = pd.DataFrame(cur.fetchall(), columns=['ItemName', 'ItemDescription',
#                                                    'LowestBidLimit', 'HighestBidderAmount'])

#         con.close()

#         return render_template("List_Auction_Items.html", rows=df)


# # add a new Auction item page of website function that renders 'Add_a_new_Auction_Item.html'
# # if the user has app role level 1, 2, or 3
# @app.route('/Add_a_new_Auction_Item')
# def add_Item():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
#         # else takes user to the login page
#         return render_template('Login.html')
#     else:
#         return render_template('Add_a_new_Auction_Item.html')


# # the function extract the bidder information from
# # what the user submit in the 'AAdd_a_new_Auction_Item.html' page
# # if the user has app role level 1, 2, or 3
# @app.route('/additem', methods=['POST', 'GET'])
# def additem():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
#         # else takes user to the login page
#         return render_template('Login.html')
#     else:
#         if request.method == 'POST':

#             # extracts the ItemId and checks if its numeric
#             # or is greater than zero
#             # if this condition is met IDB is set to true and an error message is initialized
#             # else it is set to false
#             ID = request.form['ItemId']
#             if (not str(ID).isnumeric()) or (int(ID) <= 0):
#                 IDB = False
#                 msg_ID = "The ItemID must be a numeric value greater than 0"
#                 msg = ""
#             else:
#                 msg_ID = ""
#                 IDB = True

#             # extracts the Bid Amount and checks if its numeric
#             # or is greater than zero
#             # if this condition is met bdaB is set to true and an error message is initialized
#             # else it is set to false
#             bda = request.form['Bid Amount']
#             if (not str(bda).isnumeric()) or (int(bda) <= 0):
#                 bdaB = False
#                 msg_bda = "The Bid Amount must be a numeric value greater than 0"
#                 msg = ""
#             else:
#                 msg_bda = ""
#                 bdaB = True

#             con = sqlite3.connect('BidderDB.db')
#             # if all conditions were met it sends the message to the server
#             # to request the bid and prints Record successfully sent
#             if IDB and bdaB:
#                 if request.method == 'POST':
#                     try:
#                         msg_sent = str(session.get('BidderID')) + " " + \
#                                    request.form['ItemId'] + " " + request.form['Bid Amount']

#                         # encrypts message
#                         msg_sent = str(Encryption.cipher.encrypt(bytes(msg_sent, 'utf-8')).decode("utf-8"))

#                         HOST, PORT = "localhost", 9999
#                         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#                         sock.connect((HOST, PORT))

#                         sock.sendall(bytes(msg_sent, "utf-8"))

#                         msg = "Record successfully sent"

#                     except:
#                         msg = "Error-Bid NOT sent"
#                     finally:
#                         sock.close()
#                 con.commit()
#             # else rolls back
#             else:
#                 con.rollback()
#             con.close()

#             # displays if the task was successful else display the errors in "Results.html" page
#             return render_template("Results.html", msg=msg, msg_ID=msg_ID, msg_bda=msg_bda)


# # send bid with authentication website function that renders 'Send_Bid_HMAC_Encryption.html'
# # if the user has app role level 1, 2, or 3
# @app.route('/Send_Bid_HMAC_Encryption')
# def SendBidHMAC():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
#         # else takes user to the login page
#         return render_template('Login.html')
#     else:
#         return render_template('Send_Bid_HMAC_Encryption.html')


# # the function extract the bidder information from
# # what the user submit in the 'Send_Bid_HMAC_Encryption.html' page
# # if the user has app role level 1, 2, or 3
# @app.route('/sendBidHMAC', methods=['POST', 'GET'])
# def sendBidHMAC():
#     if not session.get('logged_in1') and not session.get('logged_in2') and not session.get('logged_in3'):
#         # else takes user to the login page
#         return render_template('Login.html')
#     else:
#         if request.method == 'POST':

#             # extracts the ItemId and checks if its numeric
#             # or is greater than zero
#             # if this condition is met IDB is set to true and an error message is initialized
#             # else it is set to false
#             ID = request.form['ItemId']
#             if (not str(ID).isnumeric()) or (int(ID) <= 0):
#                 IDB = False
#                 msg_ID = "The ItemID must be a numeric value greater than 0"
#                 msg = ""
#             else:
#                 msg_ID = ""
#                 IDB = True

#             # extracts the Bid Amount and checks if its numeric
#             # or is greater than zero
#             # if this condition is met bdaB is set to true and an error message is initialized
#             # else it is set to false
#             bda = request.form['Bid Amount']
#             if (not str(bda).isnumeric()) or (int(bda) <= 0):
#                 bdaB = False
#                 msg_bda = "The Bid Amount must be a numeric value greater than 0"
#                 msg = ""
#             else:
#                 msg_bda = ""
#                 bdaB = True

#             con = sqlite3.connect('BidderDB.db')
#             # if all conditions were met it sends the message to the server
#             # to request the bid and prints Record successfully sent
#             if IDB and bdaB:
#                 if request.method == 'POST':
#                     try:

#                         msg_sent = str(session.get('BidderID')) + " " + \
#                                    request.form['ItemId'] + " " + request.form['Bid Amount']

#                         HOST, PORT = "localhost", 8888
#                         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#                         sock.connect((HOST, PORT))

#                         # encrypts message
#                         msg_sent_E = Encryption.cipher.encrypt(bytes(msg_sent, 'utf-8'))

#                         secret = b'1234'

#                         # creates tag
#                         H_msg = hmac.new(secret, bytes(msg_sent, 'utf-8'), digestmod=hashlib.sha3_512).digest()


#                         sent_msg = msg_sent_E + H_msg

#                         sock.sendall(sent_msg)

#                         msg = "Record successfully sent"
#                     except:
#                         msg = "Error-Bid NOT sent"
#                     finally:
#                         sock.close()
#                 con.commit()
#             # else rolls back
#             else:
#                 con.rollback()
#             con.close()

#             # displays if the task was successful else display the errors in "Results.html" page
#             return render_template("Results.html", msg=msg, msg_ID=msg_ID, msg_bda=msg_bda)
