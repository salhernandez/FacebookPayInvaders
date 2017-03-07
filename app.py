import os
import sys
import json
import requests
from flask import Flask, render_template, request
import flask_sqlalchemy
app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#db = flask_sqlalchemy.SQLAlchemy(app)
import models

@app.route('/data')
def hello():
    
    message = models.Users.query.all()
    print message
    return render_template('index.html')

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


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
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

                if messaging_event.get("message"):  # someone sent us a message
                    
                    #hardcode josh's fb id
                    #sender_id = str(985245348244242)
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    
                    message_text = messaging_event["message"]["text"]  # the message's text
                    #message_timestamp = messaging_event["timestamp"]  # the message's timestamp
                    #time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(message_timestamp))))
                    
                    #get the name of the sender
                    senderName = getNameOfUser(str(sender_id))
                    
                    #loooks for the user id
                    payed_id, userFirst = getIDofUser(message_text)
                    
                    #gets the amount from the string
                    amount = getAmount(message_text)
                    
                    #if there is no name and amount, it will reply to the user with a static response
                    
                    #checks that the user and the amount is there
                    if payed_id is not False and amount is not False and senderName is not False:
                        #let the user know that they payed the person
                        send_message(sender_id, "you paid $"+str(amount)+" to "+userFirst)
                        
                        #sned the message to the person who got payed
                        send_message(payed_id, "got paid $"+str(amount)+" by "+senderName)
                    
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
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        
def getAmount(data):
    #get words in string
    splits = data.split(" ")
    amount  = False
    #grab the word that has the $ char
    for word in splits:
        if '$' in word:
            #get number
            amount =  word[1:]
            break
    
    return amount
    
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
