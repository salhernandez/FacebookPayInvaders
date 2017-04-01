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


class MessageBuilder(object):
    def __init__(self, **kwargs):
        self.fromUser = kwargs.get('fromUser', "-1")
        self.toUser = kwargs.get('toUser', "-1")
        # self.toUser2 = kwargs.get('toUser2', "-1")
        self.messageType = kwargs.get('messageType', "-1")
        self.messageText = kwargs.get('messageText', "-1")
        self.amount = kwargs.get('amount', -1)

        self.defaultMessage = "You can ask me to pay someone, request money from someone, split a bill, or clear all previous commands"
        # checks if the fromUser object was passed or not
        # if not it would bean that the message is strictly from the bot to the user

        self.fromName = self.fromUser.name
        self.toName = self.toUser.name

        self.fromID = self.fromUser.ID
        self.toID = self.toUser.ID

    def message_template_simple(self, toID, messageText):
        msg1 = "sending message to {recipient}: {text}".format(recipient=toID, text=messageText)
        self.log(msg1)

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
        dataDict = {}
        dataDict['recipient'] = {}
        dataDict['message'] = {}

        dataDict['recipient']['id'] = str(toID)
        dataDict['message']['text'] = str(messageText)

        data = json.dumps(dataDict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    ##send message to user 
    ############################################################################
    def send_default_message(self):
        self.message_template_simple(self.fromID, self.defaultMessage)

    def send_request_from_who_message(self):
        self.message_template_simple(self.fromID, "Who would you like to request money from?")
    
    def send_pay_who_message1(self):
        self.message_template_simple(self.fromID, "Who would you like to pay?")
    
    def send_pay_who_message2(self):
        self.message_template_simple(self.fromID, "Who would you like to pay $" + self.amount + "?")

    def send_split_message(self):
        self.message_template_simple(self.fromID, "Who would you like to split the bill with?")

    def send_split_how_many_ways(self):
        self.message_template_simple(self.fromID, "How may ways would you like to split the bill?")

    def send_clear_message(self):
        self.message_template_simple(self.fromID, "The conversation has been cleared! " + self.defaultMessage)

    def send_how_much_message(self):
        self.message_template_simple(self.fromID, "Please specify an amount")

    def send_payment_log_message(self):
        self.message_template_simple(self.fromID, "You paid $" + self.amount + " to " + self.toName)

    def send_confirmation_message(self):
        self.message_template_simple(self.fromID, "Please confirm this action by typing '<action> <name> <amount>'?")

    def send_payment_made_message(self):
        self.message_template_simple(self.toID, "You got paid $" + self.amount + " from " + self.fromName)
        
    def send_split_log_message(self):
        self.message_template_simple(self.fromID, "You requested to split the bill with " + self.toName)
        
    def send_split_made_message(self):
        self.message_template_simple(self.toID, self.fromName + " requested to split the bill with you")    
        
    def send_request_log_message(self):
        self.message_template_simple(self.fromID, "You requested $" + self.amount + " from " + self.toName)

    def send_request_made_message(self):
        self.message_template_simple(self.toID, self.fromName + " requested $" + self.amount + " from you")    

    def send_share_link_message(self):
        self.message_template_simple(self.fromID,
                                     "Hm, it looks like this user isn't in my system. Make sure they interact with me at " +
                                     "https://www.facebook.com/IAmPayBot/")

    def send_split_with_who_message(self):
        self.message_template_simple(self.fromID, "Who would you like to split the bill with?")

    def notify_payee_and_payer_of_payment(self):
        self.send_payment_made_message()
        self.send_payment_log_message()
        
    def notify_requestee_and_requester_of_request(self):
        self.send_request_made_message()
        self.send_request_log_message()
        
    def notify_bill_splitters_of_request(self):
        self.send_split_made_message()
        self.send_split_log_message()
    ############################################################################
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)