import os, sys, requests, json

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
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"What do you want to do?", "quick_replies":[ { "content_type":"text", "title":"Pay", "payload":" 'responseType':'action', 'value':'pay' " }, { "content_type":"text", "title":"Request", "payload":" 'responseType':'action', 'value':'request' " }, { "content_type":"text", "title":"Split", "payload":" 'responseType':'action', 'value':'split' " } ] } }"""        #gets rid of white space
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
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"What do you want to do?", "quick_replies":[ { "content_type":"text", "title":"Confirm", "payload":" 'responseType':'confirmDeny', 'value':'confirm' " }, { "content_type":"text", "title":"Deny", "payload":" 'responseType':'confirmDeny', 'value':'deny' " } ] } }"""
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
    
    def send_users_quick_reply(self, toID, users):

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

        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Who would you like to message?","quick_replies":[{"content_type":"text","title":"Josh","payload":"{'responseType':'josh', 'value': '22'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
       
        for i in range(len(users)-1):
            JSON_Datalist = JSON_Datalist + """,{"content_type":"text","title":"Josh","payload":"{'responseType':'josh', 'value': '22'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
        JSON_Datalist = JSON_Datalist + """]}}"""
        
        the_dict = json.loads(JSON_Datalist)

        the_dict['recipient']['id'] = str(toID)
        for i in range(len(users)-1):
            payloadDict = {}
            
            the_dict['message']['quick_replies'][i]['title'] = str(users[i]['firstName'])
            the_dict['message']['quick_replies'][i]['image_url'] = str(users[i]['imgUrl'])
            the_dict['message']['quick_replies'][i]['payload'] = {}
            the_dict['message']['quick_replies'][i]['payload']['responseType'] = "selectedPerson"
            the_dict['message']['quick_replies'][i]['payload']['value'] = users[i]['userID']
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