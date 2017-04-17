import json

#This class is used specidifcally for taking apart the message and get the info
#we want from it. 

class MessageParser(object):
    def __init__(self, msg):
        self.ogMsg = msg
        self.__getNumber__(self.ogMsg)
        self.__getAmount__(self.ogMsg)
        self.__getIDofUser__(self.ogMsg)

    def getMessage(self):
        return self.ogMsg
            
    def __getIDofUser__(self,someText):
        
        print type(someText.lower())
        someText = str(someText.lower())
        userID = "-1"
        userFirst = ""
        
        print someText
        
        
        if 'josh' in someText:
            userID = str(985245348244242)
            userFirst = "josh"

        elif 'sal' in someText:
            userID = str(1596606567017003)
            userFirst = "sal"

        elif 'anna' in someText:
            userID = str(1204927079622878)
            userFirst = "anna"
        

        # else:
        #     userID = "-1"
        #     userFirst = ""

        self.userID = userID
        self.userFirst = userFirst
        
    def __getAmount__(self,data):
        # get words in string
        splits = data.split(" ")
        amount = "-1"
        # grab the word that has the $ char
        for word in splits:
            if '$' in word:
                # get number
                amount = word[1:]
                break

        self.amount = amount

    def __str__(self):
        return str(self.__dict__)
        
    def __getNumber__(self, data):
        # get words in string
        splits = data.split(" ")
        number = "-1"
        # grab the word that has the $ char
        for word in splits:
            if '!!' in word:
                # get number
                number = word[2:]
                break

        self.number = number

    def __str__(self):
        return str(self.__dict__)
        