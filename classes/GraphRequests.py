import requests, os, json

# This class is meant to containt all the graph request that we will use

#sample usage
# aTest = GraphRequests.GraphRequests()
# aTest.getUserInfo(1204927079622878)
# print str(aTest)

class GraphRequests(object):
    def __init__(self):
        pass
    #gets user's info and returns it in json format
    def getUserInfo(self, userID):
        self.userID = str(userID)
        prepLink = 'https://graph.facebook.com/v2.8/'+self.userID
        
        params = (
            ('access_token', os.getenv('PAGE_ACCESS_TOKEN')),
        )
        
        response = requests.get(prepLink, params=params)
        data  = response.json()
        
        #all the information that can be grabbed from the user
        self.firstName = data['first_name']
        self.lastName = data['last_name']
        self.profile_pic = data['profile_pic']
        self.locale = data['locale']
        self.timezone = data['timezone']
        self.gender = data['gender']
        
    def __str__(self):
        return str(self.__dict__)