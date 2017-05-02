import os, sys, requests, json

class QuickReply(object):
    def __init__(self):
        pass
    
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
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"Options:", "quick_replies":[ { "content_type":"text", "title":"Confirm", "payload":" 'responseType':'confirmDeny', 'value':'confirm' " }, { "content_type":"text", "title":"Deny", "payload":" 'responseType':'confirmDeny', 'value':'deny' " } ] } }"""
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
        self.log(users)

        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Choose a friend","quick_replies":[{"content_type":"text","title":"not here","payload":"{'responseType':'selectedperson','value':'nothere'}","image_url":"https://nothere.me/app/themes/roots/assets/img/brandmark.svg"}"""
        totalPpl = 0
        for i in range(len(users)):
            self.log(str(i))
            totalPpl = totalPpl +1
            JSON_Datalist = JSON_Datalist + """,{"content_type":"text","title":"x","payload":"{'responseType':'selectedperson','value':'default'}}","image_url":"https://nothere.me/app/themes/roots/assets/img/brandmark.svg"}"""
        JSON_Datalist = JSON_Datalist + """]}}"""
        the_dict = json.loads(JSON_Datalist)
        
        #different access
        if totalPpl == 1:
            self.log("begin")
            for key, value in users.iteritems():
                self.log("key 1: "+str(key))
                self.log("value 1: "+str(value))
                for key_2, value_2 in value.iteritems():
                    self.log("key 2: "+str(key_2))
                    self.log("value 2: "+str(value_2))
                    for key_3, value_3 in value_2.iteritems():
                        if key_3 in "firstName":
                            the_dict['message']['quick_replies'][1]['title'] = str(value_3)
                        elif key_3 in "lastName":
                            temp = the_dict['message']['quick_replies'][1]['title']
                            the_dict['message']['quick_replies'][1]['title'] = temp+" "+str(value_3)
                        elif key_3 in "imgUrl":
                            the_dict['message']['quick_replies'][1]['image_url'] = str(value_3)
                        elif key_3 in "userID":
                            the_dict['message']['quick_replies'][i+1]['payload'] = "'responseType': 'selectedPerson', 'value': '" + str(value_3) + "'"
        
        else:    
            for i in range(len(users)):
                self.log(str(i))
                the_dict['message']['quick_replies'][i+1]['title'] = users[i]['firstName']
                the_dict['message']['quick_replies'][i+1]['image_url'] = users[i]['imgUrl']
                the_dict['message']['quick_replies'][i+1]['payload'] = "{'responseType': 'selectedPerson', 'value': " + str(users[i]['userID']) + "}"
        
        the_dict['recipient']['id'] = str(toID)
        data = json.dumps(the_dict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    """
    Sends a quick reply with the buttons "yes", "no" with the proper payload
    
    aReply = QuickReply.QuickReply()
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
        JSON_Datalist = """{ "recipient":{ "id":"USER_ID" }, "message":{ "text":"What do you want to do?", "quick_replies":[ { "content_type":"text", "title":"Pay", "payload":" 'responseType':'action', 'value':'pay' " }, { "content_type":"text", "title":"Request", "payload":" 'responseType':'action', 'value':'request' " }, { "content_type":"text", "title":"Split", "payload":" 'responseType':'action', 'value':'split' " } ] } }"""
        JSON_Datalist = JSON_Datalist.replace(" ", "")
        the_dict = json.loads(JSON_Datalist)
        the_dict['recipient']['id'] = str(toID)
        the_dict['message']['text'] = "What do you want to do?"
        

        data = json.dumps(the_dict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    """
    Sends a quick reply with the buttons "Confirm", "Deny" with the proper payload
    
    aReply = QuickReply.QuickReply()
    aReply.send_yesNo_quick_reply("1596606567017003")
    """
    def send_yesNo_quick_reply(self, toID):
        
        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        # convert dict into json
        #####################################
        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Add Another Person?","quick_replies":[{"content_type":"text","title":"yes","payload":"'responseType':'yesno','value':'yes'"},{"content_type":"text","title":"no","payload":"'responseType':'yesno','value':'no'"}]}}"""
        #gets rid of white space
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
            
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)