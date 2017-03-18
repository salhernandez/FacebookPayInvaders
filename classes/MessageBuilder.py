import json, os, sys, requests


class MessageBuilder(object):
    def __init__(self, **kwargs):
        self.fromUser = kwargs.get('fromUser', None)
        self.toUser = kwargs.get('toUser', "default value")
        self.messageType = kwargs.get('messageType', "default value")
        self.messageText = kwargs.get('messageText', "default value")
        self.amount = kwargs.get('amount', 0.0)

        self.defaultMessage = "sup"
        # checks if the fromUser object was passed or not
        # if not it would bean that the message is strictly from the bot to the user
        if self.fromUser is not None:
            self.fromName = self.fromUser.name
            self.toName = self.toUser.name

        self.fromID = self.fromUser.ID
        self.toID = self.toUser.ID

    def message_template_simple(self, toID, messageText):
        msg1 = "sending message to {recipient}: {text}".format(recipient=toID, text=messageText)
        self.__log__(msg1)

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
            self.__log__(r.status_code)
            self.__log__(r.text)

    def send_default_message(self):
        self.message_template_simple(self.toID, self.defaultMessage)

    def send_payment_log_message(self):
        self.message_template_simple(self.fromID, "you paid $" + self.amount + " to " + self.toName)

    def send_payment_made_message(self):
        self.message_template_simple(self.toID, "got paid $" + self.amount + " from " + self.fromName)

    def send_share_link_message(self):
        self.message_template_simple(self.toID,
                                     "The user you are trying to pay is not in the system, make sure they interact with me at " +
                                     "https://www.facebook.com/IAmPayBot/")
    def notify_payee_and_payer_of_payment(self):
        self.send_payment_made_message()
        self.send_payment_log_message()


    def __log__(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()