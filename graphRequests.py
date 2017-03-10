import requests
import os
import json

#gets user's info and returns it in json format
def requestUserInfo(userID):
    prepLink = 'https://graph.facebook.com/v2.8/'+str(userID)
    
    params = (
        ('access_token', os.getenv('PAGE_ACCESS_TOKEN')),
    )
    
    
    response = requests.get(prepLink, params=params)
    data  = response.json()
    
    return data
    #all the information that can be grabbed from the user
    # print data['first_name']
    # print data['last_name']
    # print data['profile_pic']
    # print data['locale']
    # print data['timezone']
    # print data['gender']
    

#print requestUserInfo(1204927079622878)