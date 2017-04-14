import requests, os, json

# This class is meant to containt all the graph request that we will use

# Sample Usage
# aReplyParser = QuickReplyParser.QuickReplyParser("1596606567017003", "pay", 1)
# print str(aReplyParser)
class QuickReplyParser(object):
    def __init__(self, flowType, flowState, senderID):
        self.flowType = str(flowType).lower()
        self.flowState = flowState
        self.senderID = senderID
    
    """
    prints the instance variables as a dictionary
    """
    def __str__(self):
        return str(self.__dict__)