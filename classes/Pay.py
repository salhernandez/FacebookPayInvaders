import json, os, sys, requests

#all in order to send a message to a user, you need to initialize the MessageBuilder witht the user objects,
#the sendUser object will always be there, but not the payedUser. The class is based on kwargs
#after initializing the class you can call on the send functions to either share a link or notify of payments

#if all you want to do is initialize the object to send a simple message, make
#sure to initialize the object with a fromUser UserInfo object
#otherwise it will not have the neccesaruy information to send a message

## simple sample
## create userInfo object
#senderUser = UserInfo.UserInfo("sal", str(1596606567017003))
## pass it into MessageBuilder 
#sendMsg = MsgBuilder.MessageBuilder(fromUser = senderUser)
## send message to user
#sendMsg.send_default_message()


class PayGate(object):
    def __init__(self, **kwargs):
        self.toUser = kwargs.get('toUser', "-1")
        # self.toUser2 = kwargs.get('toUser2', "-1")

        self.defaultMessage = "You can ask me to pay someone, request money from someone, split a bill, or clear all previous commands"
        # checks if the fromUser object was passed or not
        # if not it would bean that the message is strictly from the bot to the user

        self.toID = self.toUser

    def message_template_simple(self, toID):

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

        # convert dict into json
        #####################################
        JSON_Datalist = """{
             attachment: {
                "type": "template",
                "payload": {
                  "template_type": "generic",
                  "elements": [{
                    "title": "rift",
                    "subtitle": "Next-generation virtual reality",
                    "item_url": "https://www.oculus.com/en-us/rift/",               
                    "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
                    "buttons": [{
                      "type": "web_url",
                      "url": "https://www.oculus.com/en-us/rift/",
                      "title": "Open Web URL"
                    }, {
                      "type": "postback",
                      "title": "Call Postback",
                      "payload": "Payload for first bubble",
                    }],
                  }, {
                    "title": "touch",
                    "subtitle": "Your Hands, Now in VR",
                    "item_url": "https://www.oculus.com/en-us/touch/",               
                    "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                    "buttons": [{
                      "type": "web_url",
                      "url": "https://www.oculus.com/en-us/touch/",
                      "title": "Open Web URL"
                    }, {
                      "type": "postback",
                      "title": "Call Postback",
                      "payload:" "Payload for second bubble",
                    }]
                  }]
                }
              }
            }
        }""" 

        dataDict = {}
        dataDict['recipient'] = {}
        dataDict['message'] = {}

        the_dict = json.loads(JSON_Datalist)
        dataDict['recipient']['id'] = str(toID)
        dataDict['message'] = the_dict

        data = json.dumps(dataDict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    ##send message to user 
    ############################################################################

    def send_payment_gateway(self):
        self.message_template_simple(self.toID)

    ############################################################################
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)