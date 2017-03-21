import os
import sys
import json
import requests
import time
from flask import Flask, render_template, request
import flask_sqlalchemy
import classes.MsgParser as MsgParser
#import graphRequests
import numpy as np
import pandas as pd

app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#db = flask_sqlalchemy.SQLAlchemy(app)
import models

db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/data')
def hello():
    

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
    
    message = models.Users.query.all()
    print message
    message2 = models.Pay.query.all()
    print message2
    message3 = models.Payed.query.all()
    print message3
    message4 = models.Friends.query.all()
    print message4
    
    names = {985245348244242: "Josh", 1596606567017003: "Sal", 1204927079622878: "Anna"}
    print message2[0]
    print str(message2[0]).split()
    the_account = str(message2[0]).split()
    
    print names[985245348244242]
    
    
    
    # data = np.array([['','owed','needs_to_pay', 'amount', 'one more'],
    #             ['Row1',1,2, 15, 19],
    #             ['Row2',3,4, 20, 23],
    #             ['Row2',3,3, 30, 32]])
                
    # print(pd.DataFrame(data=data[1:,1:],
    #                   index=data[1:,0],
    #                   columns=data[0,1:]))
    
    df = pd.DataFrame(columns=('','owed','owed_id','needs_to_pay','needs_to_pay_id', 'amount', 'time'))
    
    df2 = pd.DataFrame(columns=('','payer','payer_id','payed_to','payed_to_id', 'amount', 'time'))

    for i in range(len(message2)):
        the_account = str(message2[i]).split()
        df.loc[i] = [i, names[int(the_account[0])], the_account[0], names[int(the_account[1])], the_account[0], the_account[2], the_account[3]]
    print(df)

    for i in range(len(message3)):
        the_account2 = str(message3[i]).split()
        df2.loc[i] = [i, names[int(the_account2[0])], the_account2[0], names[int(the_account2[1])], the_account2[0], the_account2[2], the_account2[3]]
    print(df2)
    
    return render_template('index.html', user_info = message, pay = message2, payed = message3, friends = message4)

def getIDofUser(someText):
    usrID = False
    userFirst = ""
    if 'pay josh' in someText:
        usrID = str(985245348244242)
        userFirst = "josh"
    
    elif 'pay sal' in someText:
        usrID = str(1596606567017003)
        userFirst = "sal"
    
    elif 'pay anna' in someText:
        usrID = str(1204927079622878)
        userFirst = "anna"
    
    return usrID, userFirst


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
                    
                    #check if the user is already in the Users db
                    
                    
                    # the message's text
                    message_text = messaging_event["message"]["text"]
                    
                    # the message's timestamp
                    #message_timestamp = messaging_event["timestamp"]  
                    #time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(message_timestamp))))
                    
                    #get the name of the sender
                    senderName = getNameOfUser(str(sender_id))
                    
                    #dump string into message parser and it will grab everything it needs
                    msgObj = MsgParser.MessageParser(message_text)

                    print msgObj.getMessage()
                    
                    amount  = msgObj.amount
                    userFirst  = msgObj.userFirst
                    payed_id =  msgObj.userID
                    
                    
                    #if there is no name and amount, it will reply to the user with a static response
                    #josh stuff is beklow here
                    #checks that the user and the amount is there
                    if payed_id is not False and amount is not False and senderName is not False:
                        #record data in payed table
                        #Payed
                        ts = int(time.time())
                        #first ID is the person who got PAYED, second is PAYEE
                        payment = models.Payed(payed_id, sender_id, float(amount), ts)
                        models.db.session.add(payment)
                        models.db.session.commit()
                        
                        #let the user know that they payed the person
                        send_message(sender_id, "you paid $"+str(amount)+" to "+userFirst)
                        
                        #sned the message to the person who got payed
                        send_message(payed_id, "got paid $"+str(amount)+" by "+senderName)
                    
                    #if there is an amount but no user in system, it will ask them share the link so that they can be in the system
                    elif payed_id is False and amount is not False and senderName is not False:
                        #let the user know that they payed the person
                        send_message(sender_id, "The user you are trying to pay is not in the system, make sure they interact with me at "+
                        "https://www.facebook.com/IAmPayBot/")
                        
                    else:
                        send_message(sender_id, "sup")
                    
                    
                    #get user's info
                    #getUserInfo(sender_id)
                    
                    #send share button
                    #send_share_button(sender_id)

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