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
        JSON_Datalist = """{"recipient":{"id":"recipientId"},"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Venmo","subtitle":"Please make your payment with Venmo","item_url":"https://venmo.com","image_url":"http://cdn.hercampus.com/s3fs-public/2013/09/22/venmo%201.gif","buttons":[{"type":"web_url","url":"https://venmo.com/account/sign-in","title":"Pay"},{"type":"postback","title":"Call Postback","payload":"Payload for first bubble"}]}]}}}}""" 
    
        the_dict = json.loads(JSON_Datalist)
        the_dict['recipient']['id'] = str(toID)

        data = json.dumps(the_dict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
            
    def get_user_template_simple(self, toID, users):

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

        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Who would you like to message?","quick_replies":[{"content_type":"text","title":"Josh","payload":{"responseType":"selectedPerson"},"image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
       
        for i in range(len(users)-1):
            JSON_Datalist = JSON_Datalist + """,{"content_type":"text","title":"Josh","payload":"{'responseType':'stuff'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
        JSON_Datalist = JSON_Datalist + """]}}"""
        
        the_dict = json.loads(JSON_Datalist)

        the_dict['recipient']['id'] = str(toID)
        for i in range(len(users)-1):
            the_dict['message']['quick_replies'][i]['title'] = users[i]['firstName']
            the_dict['message']['quick_replies'][i]['image_url'] = users[i]['imgUrl']
            # the_dict['message']['quick_replies'][i]['payload']['value'] = str(users[i]['userID'])
            # print the_dict['message']['quick_replies'][i]['payload']['value']

        data = json.dumps(the_dict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    ##send message to user 
    ############################################################################

    def send_payment_gateway(self):
        self.message_template_simple(self.toID)
        
    def send_user_table(self, users):
        self.get_user_template_simple(self.toID, users)

    ############################################################################
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)