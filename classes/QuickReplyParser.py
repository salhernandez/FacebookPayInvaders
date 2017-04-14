import requests, os, json, sys



# This class is meant to containt all the graph request that we will use

# Sample Usage
# aReplyParser = QuickReplyParser.QuickReplyParser("1596606567017003", "pay", 1)
# print str(aReplyParser)
class QuickReplyParser(object):
    def __init__(self, flowTypeFromResponse, valueFromResponse, senderID):
        self.flowTypeFromResponse = str(flowTypeFromResponse).lower()
        self.valueFromResponse = str(valueFromResponse).lower()
        self.senderID = senderID
        
    
    """
    is the quick reply valid
    """
    def isQRValid(self):
        self.log("entering isQRValid")
        self.log("__"+self.valueFromResponse+"__")
        isValid = False
        
        if self.valueFromResponse in "pay":
            self.__payFlow__()
            isValid = True
        elif self.valueFromResponse in "request":
            self.__requestFlow__()
            isValid = True
        elif self.valueFromResponse in "split":
            self.__splitFlow__()
            isValid = True
        else:
            isValid = False
        
        return isValid
    """
    payFlow
    """
    def __payFlow__(self):
        self.log("its the pay flow :)")
    
    """
    requestFLow
    """
    def __requestFlow__(self):
        self.log("its the request flow :)")
    
    """
    splitFLow
    """
    def __splitFlow__(self):
        self.log("its the split flow :)")
    
    """
    prints the instance variables as a dictionary
    """
    def __str__(self):
        return str(self.__dict__)
    
    def log(self, message):  # simple wrapper for logging to stdout on heroku
        print str(message)
        sys.stdout.flush()