import os
import sys
import json
import requests
import time
from flask import Flask, render_template, request, jsonify
import flask_sqlalchemy
import classes.MsgParser as MsgParser
import classes.UserInfo as UserInfo
import classes.MessageBuilder as MsgBuilder
#import graphRequests
import numpy as np
import pandas as pd

app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#db = flask_sqlalchemy.SQLAlchemy(app)
import models

db = flask_sqlalchemy.SQLAlchemy(app)

SENTINEL = "-1"
SENTINEL_FLOAT = -1.0

@app.route('/data')
def hello():
    
    # give ID's a name
    names = {985245348244242: "Josh", 1596606567017003: "Sal", 1204927079622878: "Anna"}
    
    # payedUser = UserInfo.UserInfo(names[int(request.form['pid'])], str(request.form['pid']))
    # senderUser = UserInfo.UserInfo(names[int(request.form['fid'])], str(request.form['fid']))
    # sendMsg = MsgBuilder.MessageBuilder(fromUser = senderUser, toUser = payedUser, messageType="simple", amount = str(request.form['amount']))
    # sendMsg.notify_payee_and_payer_of_payment()
    # used to insert values into database
    ########################################################################
    # # Pay
    # ts = int(time.time())
    # payment = models.Pay("985245348244242", "1596606567017003", 25.99, ts)
    # models.db.session.add(payment)
    # models.db.session.commit()
    
    # # Payed
    # ts = int(time.time())
    # payment = models.Payed("985245348244242", "1596606567017003", 25.99, ts)
    # models.db.session.add(payment)
    # models.db.session.commit()
    
    # new_user = models.Users("985245348244242", "Joshua Smith", "josmith@csumb.edu", "nope.png")
    # models.db.session.add(new_user)
    
    # new_user = models.Users("1596606567017003", "Salvador Hernandez", "salvhernandez@csumb.edu", "nope.png")
    # models.db.session.add(new_user)
    
    # new_user = models.Users("1204927079622878", "Anna Pomelov", "apomelovz@csumb.edu", "nope.png")
    # models.db.session.add(new_user)
    
    # models.db.session.commit()
    ##############################################################################################
    
    # get data from database
    message = models.Users.query.all()
    print message
    message2 = models.Pay.query.all()
    print message2
    message3 = models.Payed.query.all()
    print message3
    message4 = models.Friends.query.all()
    print message4
    

    print message2[0]
    print str(message2[0]).split()
    
    # create columns for the pay table
    df = pd.DataFrame(columns=('','owed','owed_id','needs_to_pay','needs_to_pay_id', 'amount', 'time'))
    # create columns for the payed table
    df2 = pd.DataFrame(columns=('','payer','payer_id','payed_to','payed_to_id', 'amount', 'time'))

    # make columns for the friends table
    df3 = pd.DataFrame(columns=('','id','fname', 'lname','email','pic_url'))
    
    # populate the pay dataframe
    for i in range(len(message2)):
        the_account = str(message2[i]).split()
        df.loc[i] = [i, names[int(the_account[0])], the_account[0], names[int(the_account[1])], the_account[0], float(the_account[2]), the_account[3]]
    # print(df)

    # populate the payed dataframe
    for i in range(len(message3)):
        the_account2 = str(message3[i]).split()
        df2.loc[i] = [i, names[int(the_account2[0])], the_account2[0], names[int(the_account2[1])], the_account2[0], float(the_account2[2]), the_account2[3]]
    # print(df2)
    
    # populate the friends dataframe
    for i in range(len(message)):
        the_account3 = str(message[i]).split()
        df3.loc[i] = [i, the_account3[0], the_account3[1], the_account3[2], the_account3[3], the_account3[4]]
    print(df3)

    # group and sum the pay table
    g1 = df.groupby(["owed", "needs_to_pay"], as_index=False).agg({'amount':'sum'}).convert_objects(convert_numeric=True)
    # print g1
    
    # group and sum the payed table
    g2 = df2.groupby(["payer", "payed_to"], as_index=False).agg({'amount':'sum'}).convert_objects(convert_numeric=True)
    # print g2
    
    # subtract and see who owes who
    g3 = g1[['owed', 'needs_to_pay']]
    g3['amount_to_pay'] = g1.amount - g2.amount
    
    # print g3
    
    return render_template('index.html', user_info = df3.to_html(), pay = df.to_html(), payed = df2.to_html(), owed = g3.to_html(), friends = message4)

# def getIDofUser(someText):
#     #convert string to all lower case for easier processing 
#     someText = someText.lower()
#     usrID = False
#     userFirst = ""
#     if 'pay josh' or 'make payment to josh' in someText:
#         usrID = str(985245348244242)
#         userFirst = "josh"
    
#     elif 'sal' or 'pay sal' or 'make payment to sal' in someText:
#         usrID = str(1596606567017003)
#         userFirst = "sal"
    
#     elif 'anna' or 'pay anna' or 'make payment to anna' in someText:
#         usrID = str(1204927079622878)
#         userFirst = "anna"
    
#     return usrID, userFirst


def getNameOfUser(anID):
    userFirst = False
    if str(985245348244242) in anID:
        userFirst = "josh"
    
    elif str(1596606567017003) in anID:
        userFirst = "sal"
    
    elif str(1204927079622878) in anID:
        userFirst = "anna"
    
    return userFirst

#check if user is in db, if it is burp return the data
#else False
def isUserInDB(userID):
    data = False
    message = models.Users.query.all()
    for row in message:
        if userID == row.user_id:
            data = row
            break
    return data
    
    

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    
    #for testing locally
    ##################################
    # lookupID = str(1404067442998973) #cody
    
    # user = isUserInDB(lookupID)
    
    # #if the user does not exist in the db, make graph call
    # if user is False:
    #     newUser = graphRequests.requestUserInfo(lookupID)
        
    #     print newUser
    #     #preprocess data
    #     fullName = newUser['first_name'] +" "+ newUser['last_name']
        
    #     #add data to the db
    #     new_user = models.Users(lookupID, fullName, "google@gmail.com", newUser['profile_pic'])
    #     models.db.session.add(new_user)
    #     models.db.session.commit()
        
    ##################################
    
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    
    #  This is used to save data to the database
    #  massage = models.Message(json.dumps(data, ensure_ascii=False))
    #  models.db.session.add(massage)
    #  models.db.session.commit()
    
    #   this gets data from the database
    #   messages = models.Message.query.all()
    #   new = json.loads(str(messages[0]))
    
    
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                # someone sent us a message
                if messaging_event.get("message"):
                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    
                    #check if recipient user is already in the Users db
                    #if isUserInDB(recipient_id) == false
                    #add new user to db
                    
                    # the message's text
                    message_text = messaging_event["message"]["text"]
                    
                    # the message's timestamp
                    #message_timestamp = messaging_event["timestamp"]  
                    #time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(message_timestamp))))
                    
                    #dump string into message parser and it will grab everything it needs
                    msgObj = MsgParser.MessageParser(message_text)
                    
                    #get the name of the sender
                    senderName = getNameOfUser(str(sender_id))
                    
                    #create a user object with the information obtained t from the sender
                    senderUser = UserInfo.UserInfo(senderName, sender_id)
                    
                    log("amount from string $"+ msgObj.amount)
                    
                    #dump string into message parser and it will grab everything it needs
                    msgObj = MsgParser.MessageParser(message_text)

                    print msgObj.getMessage()
                    
                    payedUser = UserInfo.UserInfo( msgObj.userFirst, msgObj.userID)
                    
                    #messageBuilder takes in kwargs as arguments, its up to the developer to keep track of the variables that have been used or not
                    #and make the proper calls for now
                    #initialze message builder
                    sendMsg = MsgBuilder.MessageBuilder(fromUser = senderUser, toUser = payedUser, messageType="simple", amount = msgObj.amount)
                    
                    #if there is no name and amount, it will reply to the user with a static response
                    #josh stuff is beklow here
                    #checks that the user and the amount is there
                    if sendMsg.toID not in SENTINEL and sendMsg.amount is not SENTINEL_FLOAT and senderUser.name not in SENTINEL:
                        log("notify both of payment")
                        sendMsg.notify_payee_and_payer_of_payment()
                    # if there is an amount but no user in system, it will ask them share the link so that they can be in the system
                    elif sendMsg.toName in "" and str(sendMsg.amount) not in SENTINEL:
                        # let the user know that they payed the person
                        log("share link message")
                        sendMsg.send_share_link_message()
                    
                    else:
                        log("default message")
                        sendMsg.send_default_message()

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    log("test2 {recipient}".format(recipient="derp"))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # data = json.dumps({
    #     "recipient": {
    #         "id": recipient_id
    #     },
    #     "message": {
    #         "text": message_text
    #     }
    # })
    
    #convert dict into json
    #####################################
    dataDict = {}
    dataDict['recipient'] = {}
    dataDict['message'] = {}
    
    dataDict['recipient']['id'] = str(recipient_id)
    dataDict['message']['text'] = str(message_text)
    
    data = json.dumps(dataDict)
    #######################################
    
    #send share button
    #########################################
    # dataDict = {}
    # dataDict['recipient'] = {}
    # dataDict['message'] = {}
    
    # dataDict['recipient']['id'] = str(recipient_id)
    # dataDict['message']['attachment'] = {}
    # dataDict['message']['attachment']['type'] =  "template"
    # dataDict['message']['attachment']['payload'] = {}
    # dataDict['message']['attachment']['payload']['template_type'] = "generic"
    # dataDict['message']['attachment']['payload']['elements'] = {}
    # dataDict['message']['attachment']['payload']['elements']['title'] = "teheee"
    # dataDict['message']['attachment']['payload']['elements']['subtitle'] = "ayeee"
    # dataDict['message']['attachment']['payload']['elements']['image_url'] = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    # dataDict['message']['attachment']['payload']['elements']['buttons'] = {}
    # dataDict['message']['attachment']['payload']['elements']['buttons']['type'] = "element_share"
    
    #data = json.dumps(dataDict)

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    
def getUserInfo(anId):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        str(anId)
    })
    r = requests.get("https://graph.facebook.com/v2.6/", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    else:
        log("SUCCESS  "+r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(

        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )