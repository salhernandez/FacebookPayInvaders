import requests, os, json, sys, flask, flask_sqlalchemy
import classes.DBLink as DBLink

# This class is meant to containt all the graph request that we will use

# Sample Usage
# aReplyParser = QuickReplyParser.QuickReplyParser("1596606567017003", "pay", 1)
# print str(aReplyParser)

"""
methods are laid out to strip information like flow state and flow state info
based on the methods, all of the information will be stored in instance
variables but can also be returned just in case a check needs to be made,
like if a quick response is valid

#SAMPLE USE
qrParser = QuickReplyParser.QuickReplyParser("action", "split", 985245348244242)
    #isValid = qrParser.isQRActionValid()
    flowInfo = qrParser.getFlowState()
    qrParser.__getFlowStateInfo__()
    qrParser.triggerResponseTypeConditions()
"""
class QuickReplyParser(object):
    def __init__(self, responseType, valueFromResponse, senderID):
        self.responseType = str(responseType).lower()
        self.valueFromResponse = str(valueFromResponse).lower()
        self.senderID = senderID
        self.dbLink = DBLink.DBLink()
        
    
    """
    Checks if the quick reply for action is one that we need to handle
    """
    def isQRActionValid(self):
        self.log("entering isQRValid")
        accepted_strings = {'pay', 'request', 'split'}
        
        isValid = True
        
        # if self.valueFromResponse not in accepted_strings:
        #     self.log("QR in is not accepted")
        #     isValid = False
        if self.valueFromResponse in "pay":
            self.__payFlow__()
        elif self.valueFromResponse in "request":
            self.__requestFlow__()
        elif self.valueFromResponse in "split":
            self.__splitFlow__()
        else:
            isValid = False
        
        return isValid
       
    """
    Checks if the quick reply for confirm/deny is one that we need to handle
    """
    def isQRConfirmDenyValid(self):
        self.log("entering isQRConfirmDenyValid")
        accepted_strings = {'confirm', 'deny'}
        
        isValid = True
        
        # if self.valueFromResponse not in accepted_strings:
        #     self.log("QR is not accepted")
        #     isValid = False
        
        if self.valueFromResponse in "confirm":
            pass
        elif self.valueFromResponse in "deny":
            pass
        else:
            isValid = False
            
        return isValid
    
    """
    Checks if the quick reply for the selectedPerson type
    """
    def isQRSelectPersonValid(self):
        self.log("entering isQRSelectPersonValid")
        accepted_strings = {'selectedPerson'}
        
        isValid = True
        
        if self.responseType not in accepted_strings:
            self.log("QR is not selectedPerson")
            isValid = False
            
        return isValid
    
    """
    Checks if the quick reply for the selectedPerson type
    is yes or no
    """
    def isQRYesNoValid(self):
        self.log("entering isQRYesNoValid")
        accepted_strings = {'yes', 'no'}
        
        isValid = True
        
        if self.responseType not in accepted_strings:
            self.log("QR is not accepted as yes no")
            isValid = False
            
        return isValid
    
    """
    payFlow
    """
    def __payFlow__(self):
        self.log("its the pay flow :)")
        self.getFlowState()
    
    """
    requestFLow
    """
    def __requestFlow__(self):
        self.log("its the request flow :)")
        self.getFlowState()
    """
    splitFLow
    """
    def __splitFlow__(self):
        self.log("its the split flow :)")
        self.getFlowState()
    
    #confirm/deny
    def __confirmFlow__(self):
        self.log("confirmed message")
        self.getFlowState()
        
    def __denyFlow__(self):
        self.log("deny message")
        self.getFlowState()
    """
    
    getFlowInfo
    gets flow info and returns dictionary, it also puts the values in instance
    variables
    """
    def getFlowState(self):
        self.log("getting flow info :)")
        #####################################################
        #Check where sender is in flow
        
        flow_state = self.dbLink.get_flow_state(self.senderID)
        
        self.flowStateInfo = flow_state
        
        self.flowTypeFromDB = flow_state['flowType']
        self.flowStateFromDB = flow_state['flowState']
    
        #for testing values of flowstate and flowtype
        self.log("FLOWSTATE FROM DB")
        self.log(flow_state['flowState'])
        self.log("FLOWTYPE FROM DB")
        self.log(flow_state['flowType'])
        self.log(self.valueFromResponse)
        
        #return flowState
        
        return
        
        # #check if the user's flow selection matches the flowType in the db
        # if flow_type not in self.valueFromResponse:
        #     self.log("flowState sent and db flowState don't match")
        #     ##let the user know that they did not do it right
        #     ##resend request based on current flow
        
        # #if the user's flow selection matches, get the user's info from the db
        # else:
        #     self.userStateInfo = self.dbLink.get_state_info(self.senderID)
        #     self.log(self.userStateInfo)
        
        
        #####################################################
    
    """
    __getFlowStateInfo__
    puts the state info dictionary into an instance variable
    """
    def __getFlowStateInfo__(self):
        self.userStateInfo = self.dbLink.get_state_info(self.senderID)
        self.log(self.userStateInfo)
    
    """
    responseTypeConditions
    Provides the conditions for each responseType and value
    """
    def triggerResponseTypeConditions(self):
        
        #for the pay, request, split buttons
        if self.responseType in "action":
            self.log("triggered action")
        
        #for the person selection buttons
        elif self.responseType in "selectPerson":
            self.log("triggered selectPerson")
        
        #for the person selection buttons
        elif self.responseType in "confirmDeny":
            self.log("triggered confirmDeny")
    
    """
    
    """
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

        JSON_Datalist = """{"recipient":{"id":"USER_ID"},"message":{"text":"Who would you like to message?","quick_replies":[{"content_type":"text","title":"Josh","payload":"{'user':'josh'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
       
        for i in range(len(users)-1):
            JSON_Datalist = JSON_Datalist + """,{"content_type":"text","title":"Josh","payload":"{'user':'josh'}","image_url":"https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-9/14457456_10210934688542219_8214757857053421347_n.jpg?oh=5ec34a9a1eefce4482fede3274e189eb&oe=5997A28C"}"""
        JSON_Datalist = JSON_Datalist + """]}}"""
        
        the_dict = json.loads(JSON_Datalist)

        the_dict['recipient']['id'] = str(toID)
        for i in range(len(users)-1):
            the_dict['message']['quick_replies'][i]['title'] = users[i]['firstName']
            the_dict['message']['quick_replies'][i]['image_url'] = users[i]['imgUrl']
            the_dict['message']['quick_replies'][i]['payload'] = {"responseType":"selectedPerson","value":users[i]['userID']}

        data = json.dumps(the_dict)
        #######################################
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    """
    prints the instance variables as a dictionary
    """
    def __str__(self):
        return str(self.__dict__)
    
    def log(self, message):  # simple wrapper for logging to stdout on heroku
        print str(message)
        sys.stdout.flush()