import requests, os, json, sys

# This class is meant to containt all the graph request that we will use

# Sample Usage
# aReplyParser = QuickReplyParser.QuickReplyParser("1596606567017003", "pay", 1)
# print str(aReplyParser)
class QuickReplyParser(object):
    def __init__(self, flowType, flowState, senderID):
        self.flowType = str(flowType).lower()
        self.flowState = flowState
        self.senderID = senderID
        
        
        if self.flowType is "pay":
            self.__payFlow__()
        elif self.flowType is "request":
            self.__requestFlow__()
        elif self.flowType is "split":
            self.__splitFlow__()
        else:
            return None
        
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