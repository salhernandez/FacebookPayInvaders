# stores the information for oay or request classes
# it is kept for persistence of data.

# flowType = "pay" or "request"

class StateInfo(object):
    def __init__(self, senderID, recipientID, amount, flowType):
        self.senderID = str(senderID)
        self.recipientID = str(recipientID)
        self.amount = amount
        self.flowType = flowType

    def __str__(self):
        return str(self.__dict__)