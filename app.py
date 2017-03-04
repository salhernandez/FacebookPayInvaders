import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


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
                    sender_id = str(985245348244242)
                    #sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    
                    message_text = messaging_event["message"]["text"]  # the message's text
                    #message_timestamp = messaging_event["timestamp"]  # the message's timestamp
                    #time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(message_timestamp))))
                
                    #send message
                    #send_message(sender_id, message_text)
                    
                    #send share button
                    send_share_button(sender_id)

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

#send share button
def send_share_button(user_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    b = json.dumps({
        
                                "type":"element_share"
                            
        
    })
    a = json.dumps({
                        "subtitle": "tehee",
                        "image_url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        "buttons": b
                            
        })
    
    data = json.dumps({
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment":{
                "type": "template",
                "payload":{
                    "template_type":"generic",
                    "elements": a
            }
        }
        }
    })
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
