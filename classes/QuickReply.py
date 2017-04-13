import json, os, sys, requests

class QuickReply(object):
    def __init__(self):
        pass

    def send_acttion_quick_reply(self, toID):
        
        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        # convert dict into json
        #####################################
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"What do you want to do?", "quick_replies":[ { "content_type":"text", "title":"Pay", "payload":" 'flowType':'action', 'value':'pay' " }, { "content_type":"text", "title":"Request", "payload":" 'flowType':'action', 'value':'request' " }, { "content_type":"text", "title":"Split", "payload":" 'flowType':'action', 'value':'split' " } ] } }"""
        
        #gets rid of white space
        JSON_Datalist = JSON_Datalist.replace(" ", "")
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

        # convert dict into json
        #####################################
        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Who would you like to message?","quick_replies":[{"content_type":"text","title":"Josh","payload":"{'user':'josh'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"},{"content_type":"text","title":"Sal","payload":"{'user':'sal'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/12032077_888265507894236_5231089217486342060_n.jpg?oh=dd68d76329a1aad696062af30961306a&oe=595B6D4E"}]}}""" 
        
        
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