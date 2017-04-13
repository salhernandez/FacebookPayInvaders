import json, os, sys, requests

class QuickReply(object):
    def __init__(self):
        pass
    
    """
    Sends a quick reply with the buttons "Pay", "Request", "Split" with the proper payload
    
    aReply = QuickReply.QuickReply()
    aReply.send_action_quick_reply("1596606567017003")
    """
    def send_action_quick_reply(self, toID):
        
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
    
    """
    Sends a quick reply with the buttons "Confirm", "Deny" with the proper payload
    
    aReply = QuickReply.QuickReply()
    aReply.send_confirmDeny_quick_reply("1596606567017003")
    """
    def send_confirmDeny_quick_reply(self, toID):
        
        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        # convert dict into json
        #####################################
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"What do you want to do?", "quick_replies":[ { "content_type":"text", "title":"Confirm", "payload":" 'flowType':'confirmDeny', 'value':'confirm' " }, { "content_type":"text", "title":"Deny", "payload":" 'flowType':'confirmDeny', 'value':'deny' " } ] } }"""
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

    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)