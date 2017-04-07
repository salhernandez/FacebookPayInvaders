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
            
    def get_user_template_simple(self, toID):

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
        JSON_Datalist = """{"recipient":{"id":"RECIPIENT_ID"},"message":{"attachment":{"type":"template","payload":{"template_type":"list","elements":[{"title":"Classic T-Shirt Collection","image_url":"https://peterssendreceiveapp.ngrok.io/img/collection.png","subtitle":"See all our colors","default_action":{"type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/shop_collection","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"},"buttons":[{"title":"View","type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/collection","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"}]},{"title":"Classic White T-Shirt","image_url":"https://peterssendreceiveapp.ngrok.io/img/white-t-shirt.png","subtitle":"100% Cotton, 200% Comfortable","default_action":{"type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/view?item=100","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"},"buttons":[{"title":"Shop Now","type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/shop?item=100","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"}]},{"title":"Classic Blue T-Shirt","image_url":"https://peterssendreceiveapp.ngrok.io/img/blue-t-shirt.png","subtitle":"100% Cotton, 200% Comfortable","default_action":{"type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/view?item=101","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"},"buttons":[{"title":"Shop Now","type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/shop?item=101","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"}]},{"title":"Classic Black T-Shirt","image_url":"https://peterssendreceiveapp.ngrok.io/img/black-t-shirt.png","subtitle":"100% Cotton, 200% Comfortable","default_action":{"type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/view?item=102","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"},"buttons":[{"title":"Shop Now","type":"web_url","url":"https://peterssendreceiveapp.ngrok.io/shop?item=102","messenger_extensions":true,"webview_height_ratio":"tall","fallback_url":"https://peterssendreceiveapp.ngrok.io/"}]}],"buttons":[{"title":"View More","type":"postback","payload":"payload"}]}}}""" 
    # 
        the_dict = json.loads(JSON_Datalist)
        the_dict['recipient']['id'] = str(toID)

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
        
    def send_user_table(self):
        self.get_user_template_simple(self.toID)

    ############################################################################
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)