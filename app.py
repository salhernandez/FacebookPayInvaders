import os
import sys
import json
import requests
import time
from flask import Flask, render_template, request, jsonify
import flask_sqlalchemy
import classes.UserInfo as UserInfo
import classes.MessageBuilder as MsgBuilder
from classes.Pay import PayGate
import classes.GraphRequests as GraphRequests
import classes.QuickReply as QuickReply
import numpy as np
import re
import pandas as pd

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

import models

db = flask_sqlalchemy.SQLAlchemy(app)

import classes.DBLink as DBLink
import classes.QuickReplyParser as QuickReplyParser
import classes.MsgParser as MsgParser

SENTINEL = "-1"
SENTINEL_FLOAT = -1.0


@app.route('/cleanUsers', methods = ['POST', 'GET'])
def saltest():
    aReply = QuickReply.QuickReply()
    dbLink = DBLink.DBLink()
    request_info = GraphRequests.GraphRequests()
    
    #SAL
    request_info.getUserInfo("1596606567017003")
    dbLink.add_user("1596606567017003", request_info.firstName, request_info.lastName, "salvhernandez@csmub.edu", request_info.profile_pic, "6197345766")
    
    #ANNA
    request_info.getUserInfo("1204927079622878")
    dbLink.add_user("1204927079622878", request_info.firstName, request_info.lastName, "apomelovz@csumb.edu", request_info.profile_pic, "4152839158")
    
    #TALA
    request_info.getUserInfo("1207261099394590")
    dbLink.add_user("1207261099394590", request_info.firstName, request_info.lastName, "unknown@gmail.com", request_info.profile_pic, "6508628427")
    
    #JOSH
    request_info.getUserInfo("985245348244242")
    dbLink.add_user("985245348244242", request_info.firstName, request_info.lastName, "unknown@gmail.com", request_info.profile_pic, "8314285108")
    
    return "cleanUsers"
    

@app.route('/saltest', methods = ['POST', 'GET'])
def saltest():
    aReply = QuickReply.QuickReply()
    dbLink = DBLink.DBLink()
    the_users = dbLink.get_all_user_in_db()
    
    #reset user
    dbLink.update_flow("1596606567017003", "", 0)
    dbLink.delete_userID_state_info("1596606567017003")
    #aReply.send_users_quick_reply("1596606567017003", the_users)
    #dbLink.init_flow_state
    #dbLink.delete_user_from_db("1596606567017003")
    #request_info = GraphRequests.GraphRequests()
    #request_info.getUserInfo("1596606567017003")
    #dbLink.add_user("1596606567017003", request_info.firstName, request_info.lastName, "salvhernandez@csmub.edu", request_info.profile_pic, "6197345766")
    # dbLink.update_flow("1596606567017003", "", 0)
    #sendMsg.send_signedup()
    #
    
    return "test"

@app.route('/test', methods = ['POST', 'GET'])
def test():
    aReply = QuickReply.QuickReply()
    dbLink = DBLink.DBLink()
    print "#######################"
    print dbLink.init_state_info("1204927079622878", "pay")
    
    return "test"

@app.route('/data', methods = ['POST', 'GET'])
def hello():
    # 
    # give ID's a name
    names = {985245348244242: "Josh", 1596606567017003: "Sal", 1204927079622878: "Anna"}
    if request.method == 'POST':
        result = request.form
        #conditions for forms
        
        if request.form["action"] == "submit_payment":
            #payment form
            if(str(result['pid'])) is not "" and (str(result['fid'])) is not "" and (str(result['amount'])) is not "":
                print "---------PAYMENT---------"
                print "---------------------->" + str(result['pid'])
                print "---------------------->" + str(result['fid'])
                print "---------------------->" + str(result['amount'])
                payedUser = UserInfo.UserInfo(names[int(request.form['pid'])], str(request.form['pid']))
                senderUser = UserInfo.UserInfo(names[int(request.form['fid'])], str(request.form['fid']))
                sendMsg = MsgBuilder.MessageBuilder(fromUser = senderUser, toUser = payedUser, messageType="simple", amount = str(request.form['amount']))
                sendMsg.notify_payee_and_payer_of_payment()
              
                ts = int(time.time())
                payment = models.Payed(str(request.form['pid']), str(request.form['fid']), float(request.form['amount']), ts)
                models.db.session.add(payment)
                models.db.session.commit()
        
        elif request.form["action"] == "submit_request":  
            #payment form
            if(str(result['requester_id'])) is not "" and (str(result['requestee_id'])) is not "" and (str(result['request_amount'])) is not "":
                print "---------REQUEST---------"
                print "---------------------->" + str(result['requester_id'])
                print "---------------------->" + str(result['requestee_id'])
                print "---------------------->" + str(result['request_amount'])
                
                requester_User = UserInfo.UserInfo(names[int(request.form['requester_id'])], str(request.form['requester_id']))
                requestee_User = UserInfo.UserInfo(names[int(request.form['requestee_id'])], str(request.form['requestee_id']))
                
                sendMsg = MsgBuilder.MessageBuilder(fromUser = requester_User, toUser = requestee_User, messageType="simple", amount = str(request.form['request_amount']))
                sendMsg.notify_requestee_and_requester_of_request()
              
                aLink = DBLink.DBLink()
                aLink.add_request(str(request.form['requester_id']),str(request.form['requestee_id']),float(request.form['request_amount']))
            #request form
    
    user_ids = []
    message = models.Users.query.with_entities(models.Users.user_id).all()
    for theId in message:
        print theId[0]
        user_ids.append(str(theId[0]))
    print "120492707962287" in user_ids
    # get data from database
    message = models.Users.query.all()
    print message
    message2 = models.Pay.query.all()
    # print message2
    message3 = models.Payed.query.all()
    # print message3
    message4 = models.Friends.query.all()
    # print message4
    

    # print message2[0]
    # print str(message2[0]).split()
    
    # create columns for the pay table
    df = pd.DataFrame(columns=('','owed','owed_id','needs_to_pay','needs_to_pay_id', 'amount', 'time'))
    # create columns for the payed table
    df2 = pd.DataFrame(columns=('','payer','payer_id','payed_to','payed_to_id', 'amount', 'time'))

    # make columns for the friends table
    df3 = pd.DataFrame(columns=('','id','fname', 'lname','email','pic_url', 'phone_number'))
    
    # populate the pay dataframe
    for i in range(len(message2)):
        the_account = str(message2[i]).split()
        df.loc[i] = [i, names[int(the_account[0])], the_account[0], names[int(the_account[1])], the_account[1], float(the_account[2]), the_account[3]]
    # print(df)

    # populate the payed dataframe
    for i in range(len(message3)):
        the_account2 = str(message3[i]).split()
        df2.loc[i] = [i, names[int(the_account2[0])], the_account2[0], names[int(the_account2[1])], the_account2[1], float(the_account2[2]), the_account2[3]]
    # print(df2)
    
    # populate the friends dataframe
    for i in range(len(message)):
        the_account3 = str(message[i]).split()
        df3.loc[i] = [i, the_account3[0], the_account3[1], the_account3[2], the_account3[3], the_account3[4], the_account3[5]]
    print(df3)

    # group and sum the pay table
    g1 = df.groupby(["owed", "needs_to_pay"], as_index=False).agg({'amount':'sum'}).convert_objects(convert_numeric=True)
    print g1
    
    # group and sum the payed table
    g2 = df2.groupby(["payer", "payed_to"], as_index=False).agg({'amount':'sum'}).convert_objects(convert_numeric=True)
    # print g2
    
    # subtract and see who owes who
    g3 = g1[['owed', 'needs_to_pay']]
    g3['amount_to_pay'] = g1.amount - g2.amount
    
    # print g3
    
    return render_template('index.html', user_info = df3.to_html(), pay = df.to_html(), payed = df2.to_html(), owed = g3.to_html(), friends = message4)

# def getIDofUser(someText):
#     #convert string to all lower case for easier processing 
#     someText = someText.lower()
#     usrID = False
#     userFirst = ""
#     if 'pay josh' or 'make payment to josh' in someText:
#         usrID = str(985245348244242)
#         userFirst = "josh"
    
#     elif 'sal' or 'pay sal' or 'make payment to sal' in someText:
#         usrID = str(1596606567017003)
#         userFirst = "sal"
    
#     elif 'anna' or 'pay anna' or 'make payment to anna' in someText:
#         usrID = str(1204927079622878)
#         userFirst = "anna"
    
#     return usrID, userFirst


def getNameOfUser(anID):
    userFirst = False
    if str(985245348244242) in anID:
        userFirst = "josh"
    
    elif str(1596606567017003) in anID:
        userFirst = "sal"
    
    elif str(1204927079622878) in anID:
        userFirst = "anna"
    
    return userFirst

#check if user is in db, if it is burp return the data
#else False
def isUserInDB(userID):
    data = False
    message = models.Users.query.all()
    for row in message:
        if userID == row.user_id:
            data = row
            break
    return data
    
    

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    
    #for testing locally
    ##################################
    # lookupID = str(1404067442998973) #cody
    
    # user = isUserInDB(lookupID)
    
    # #if the user does not exist in the db, make graph call
    # if user is False:
    #     newUser = graphRequests.requestUserInfo(lookupID)
        
    #     print newUser
    #     #preprocess data
    #     fullName = newUser['first_name'] +" "+ newUser['last_name']
        
    #     #add data to the db
    #     new_user = models.Users(lookupID, fullName, "google@gmail.com", newUser['profile_pic'])
    #     models.db.session.add(new_user)
    #     models.db.session.commit()
        
    ##################################
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
    
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                log(messaging_event)
                # someone sent us a message
                if messaging_event.get("message"):
                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    
                    #quickreply fix
                    #############################################
                    # aReply = QuickReply.QuickReply()
                    # aReply = QuickReply.QuickReply()
                    # aReply.send_action_quick_reply(messaging_event["sender"]["id"])
                    # break
                    #################################################
                    
                    # #gets info from the db
                    # dbLink = DBLink.DBLink()
                    # aUserInfo = dbLink.get_user_in_db(sender_id)
                    
                    #init with empty name
                    someUser = UserInfo.UserInfo("", messaging_event["sender"]["id"])
                    # if aUserInfo is not None:
                    #     someUser = UserInfo.UserInfo(aUserInfo['firstName'], messaging_event["sender"]["id"])
                    
                        
            ############Josh
###################################################################################################
                    user_ids = []
                    message = models.Users.query.with_entities(models.Users.user_id).all()
                    for theId in message:
                        print theId[0]
                        user_ids.append(str(theId[0]))
                    
                        
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    
                    #check if recipient user is already in the Users db
                    #if isUserInDB(recipient_id) == false
                    #add new user to db
                    
                    
                    
                  #Anna's new flow code
###################################################################################################   
                    #checks that the message has a quick reply, if not, it breaks out
                    try:
                        log("QUICK REPLY ERROR CHECK")
                        
                        info = "{"+str(messaging_event['message']['quick_reply']['payload'])+"}"
                        json_acceptable_string = info.replace("'", "\"")
                        d = json.loads(json_acceptable_string)
                        
                        #CHANGE flowType to responseType 
                        #grabs the values
                        responseTypeFromResponse = str(d['responseType'])
                        valueFromResponse = str(d['value'])
                        
                        log(d)
                        log("flowType from quick reply: "+responseTypeFromResponse)
                        log("value from quick reply: "+valueFromResponse)
                        
                        #if the quickreply is awknowledged, then it breaks out of the loop
                        #dbLink = DBLink.DBLink()
                        qrParser = QuickReplyParser.QuickReplyParser(responseTypeFromResponse, valueFromResponse, sender_id)
                        isValid = qrParser.isQRActionValid()
                        isValidConfirmDeny = qrParser.isQRConfirmDenyValid()
                        isValidSelectPerson = qrParser.isQRSelectPersonValid()
                        isYesNo = qrParser.isQRYesNoValid()
                        
                        
                        aLink = DBLink.DBLink()
                        flow_info = aLink.get_flow_state(sender_id)
                        
                        someUser = UserInfo.UserInfo("",sender_id)
                        
                        anotherUser = UserInfo.UserInfo("","")
                            
                        sendMsg = MsgBuilder.MessageBuilder(fromUser = someUser, toUser = anotherUser)
                        
                        if isValid is True:
                            log("isValid is TRUE")
                            if qrParser.valueFromResponse in "pay":
                                
                                log("VALUE FROM RESPONSE IS PAY")
                                
                                aLink.init_state_info(sender_id, "pay")
                                
                                if qrParser.flowStateFromDB == 1:
                                    #increment flowState in DB
                                    a = aLink.update_flow(sender_id, "pay", 2)
                    
                                    #send pay who message
                                    sendMsg.send_pay_who_message1()
                                    break

                            elif qrParser.valueFromResponse in "request":
                                
                                aLink.init_state_info(sender_id, "request")
                                
                                if qrParser.flowStateFromDB == 1:
                                    #increment flowState in DB
                                    a = aLink.update_flow(sender_id, "request", 2)
                                    #init state info
                                    aLink.init_flow_state(sender_id)
                                    #send pay who message
                                    sendMsg.send_request_from_who_message()
                                    break
                            
                            elif qrParser.valueFromResponse in "split":
                                
                                #start of the flow
                                if qrParser.flowStateFromDB == 1:
                                    log("INSIDE QR SPLIT 1")
                                    #send message to ask the person to enter a full name
                                    sendMsg.send_request_from_who_message()
                                    #update flow
                                    #init state info
                                    aLink.init_state_info(sender_id, "split")
                                    aLink.update_flow(sender_id, "split", 2)
                                    break

                        elif isValidConfirmDeny is True:
                            if qrParser.valueFromResponse in "confirm":
                                aReply = QuickReply.QuickReply()

                                qrParser.getFlowState()
                                
                                if qrParser.flowTypeFromDB in "request":
                                    qrParser.getFlowState()

                                    aLink.update_flow(sender_id, "", 0)

                                    sendMsg.send_your_request_was_sent()
                                    aReply.send_action_quick_reply(messaging_event["sender"]["id"])   

                                    break
                                
                                if qrParser.flowTypeFromDB in "pay":
                                    aLink.update_flow(sender_id, "", 1)
                                    
                                    #set state info row to paid table
                                    state_info = aLink.get_state_info(sender_id)
                                    
                                    recipientID = state_info['recipientID']
                                    amount = state_info['amount']
                                    flowType = state_info['flowType']
                                    splitID = state_info['splitID']
                                    timeStamp = state_info['timestamp']
                                    
                                    aLink.add_payment(recipientID, sender_id, amount)
                                    
                                    aLink.delete_userID_state_info(sender_id)
                                    
                                    the_payment = PayGate(toUser = messaging_event["sender"]["id"])
                                    the_payment.send_payment_gateway()
                                    
                                    aReply.send_action_quick_reply(messaging_event["sender"]["id"])   
                                    
                                    break
                                
                                if qrParser.flowTypeFromDB in "request":
                                    aLink.update_flow(sender_id, "", 0)

                                    sendMsg.send_your_request_was_sent()
                                    break
                                
                                if qrParser.flowTypeFromDB in "request":
                                    aLink.update_flow(sender_id, "", 0)

                                    sendMsg.send_your_request_was_sent()
                                    break
                                
                                flow_info = aLink.get_flow_state(sender_id)
                                
                                #specific confirm for split
                                #add all the information from the state info onto the pay table
                                #delete from state info
                                #ask if they want to pay another person
                                if flow_info['flowType'] in "split":
                                    flow_info['flowState'] == 5:
                                        aLink.perform_request_transaction(sender_id)
                                        #ask if they want to pay another person
                                        aReply = QuickReply.QuickReply()
                                        aReply.send_yesNo_quick_reply(sender_id)
                                        #increase flow
                                        aLink.update_flow(sender_id, "", 6)
                                        break
                                    
                            elif qrParser.valueFromResponse in "deny":
                                aReply = QuickReply.QuickReply()
                                aLink.update_flow(sender_id, "", 1)
                                aLink.delete_userID_state_info(sender_id)
                                sendMsg.send_clear_message()
                                aReply.send_action_quick_reply(messaging_event["sender"]["id"])                                
                                break
                        
                        #if the reply was a person selected
                        elif isValidSelectPerson is True:
                            flow_info = aLink.get_flow_state(sender_id)
                            
                            if flow_info['flowType'] in "pay":
                                # if flow_info['flowState'] == 3:
                                #     aLink.update_flow(sender_id, "pay", 4)
                                #     sendMsg.send_how_much_message()
                                pass
                                    
                            if flow_info['flowType'] in "request":
                                pass
                            if flow_info['flowType'] in "split":
                                if flow_info['flowState'] == 3:
                                    log("SELECTED PERSON == 3")
                                    #grab the id
                                    #updates the flow
                                    aLink.update_state_info_recipient_ID(sender_id, valueFromResponse)
                                    #updates the flow state
                                    aLink.update_flow(sender_id, "split", 4)
                                    #sends next flow state
                                    sendMsg.send_enter_amount()
                        
                        #if the response is yes or no
                        elif isYesNo is True:
                            #stateInfo = aLink.get_state_info(sender_id)
                            
                            if aReply.valueFromResponse in "yes":
                                if flow_info['flowType'] in "split":
                                    #user want to charge another person
                                    if flow_info['flowState'] == 6:
                                        #reset flow to 1 and split
                                        aLink.update_flow(sender_id, "split", 1)
                                        dbLink.delete_userID_state_info(sender_id)
                                        sendMsg.send_request_from_who_message()
                                        break
                            elif aReply.valueFromResponse in "no":
                                if flow_info['flowType'] in "split":
                                    if flow_info['flowState'] == 6:
                                        #reset flow to 0
                                        aLink.update_flow(sender_id, "", 0)
                                        aLink.delete_userID_state_info(sender_id)
                                        aReply.send_action_quick_reply(sender_id)
                                    
                    except KeyError:
                        log("KEYERROR FROM REPLY")
                        
################################################################################################### 
                
                    # the message's text
                    try:
                        message_text = messaging_event["message"]["text"]
                        
                        # the message's timestamp
                        #message_timestamp = messaging_event["timestamp"]  
                        #time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(message_timestamp))))
                        
                        #dump string into message parser and it will grab everything it needs
                        msgObj = MsgParser.MessageParser(message_text)
                        
                        if str(messaging_event["sender"]["id"]) in user_ids:
                            #get the name of the sender
                            senderName = getNameOfUser(str(sender_id))
                            
                            #create a user object with the information obtained t from the sender
                            senderUser = UserInfo.UserInfo(senderName, sender_id)
                            
                            log("amount from string $"+ msgObj.amount)
                            
                            #dump string into message parser and it will grab everything it needs
                            msgObj = MsgParser.MessageParser(message_text)
                            
                            log("WHAT THE MSG OBJECT CONTAINS: "+str(msgObj))
                            
                            #print msgObj.getMessage()
                            
                            #payedUser = UserInfo.UserInfo( msgObj.userFirst, msgObj.userID)
                            
                            #messType = str(msgObj.msgType)
                            #messageBuilder takes in kwargs as arguments, its up to the developer to keep track of the variables that have been used or not
                            #and make the proper calls for now
                            #initialze message builder
                            #sendMsg = MsgBuilder.MessageBuilder(fromUser = senderUser, toUser = payedUser, messageType=messType, amount = msgObj.amount)
                            someUser = UserInfo.UserInfo("",sender_id)
                            anotherUser = UserInfo.UserInfo("","")
                                                
                            #send share link message
                            sendMsg = MsgBuilder.MessageBuilder(fromUser = someUser, toUser = anotherUser)
                                                

                            log("WHAT THE MESSAGEBUILDER OBJECT CONTAINS: "+str(sendMsg))
                            #if there is no name and amount, it will reply to the user with a static response
                            #josh stuff is beklow here
                            #checks that the user and the amount is there
                            
                            the_payment = PayGate(toUser = messaging_event["sender"]["id"])
                            
                            #triggers venmo
                            if "josh venmo demo" in message_text:
                                the_payment = PayGate(toUser = messaging_event["sender"]["id"])
                                the_payment.send_payment_gateway()
                                break
                            
                            #sends buttons with images to josh
                            if "Josh button demo" in message_text:
                                dbLink = DBLink.DBLink()
                                #the_user = dbLink.get_users_with_first_name("Hsoj")
                                the_user = dbLink.get_all_user_in_db()
                                the_payment.send_user_table(the_user)
                                # print the_user[0]
                                # print the_user[1]
                                # print the_user[3]
                                # print len(the_user)
                                break

                            #get the message, and id, check if the message containts the right info for the current flow
                            aLink = DBLink.DBLink()
                            aReply = QuickReply.QuickReply()
                            flow_info = aLink.get_flow_state(sender_id)
                            
                            if message_text.lower() in "help":
                                sendMsg.send_help_response()

                                break
                            
                            if message_text.lower() in "clear" or message_text.lower() in "exit" or message_text.lower() in "cancel":
                                aLink.update_flow(sender_id, "", 1)
                                aLink.delete_userID_state_info(sender_id)
                                sendMsg.send_clear_message()
                                aReply.send_action_quick_reply(messaging_event["sender"]["id"])                                
                                break
                            
                            # aReply = QuickReply.QuickReply()
                            # aReply.send_action_quick_reply(messaging_event["sender"]["id"])
                            
                            #if the user is not in a flow, then it send the action quick message reply

                            if flow_info['flowState'] == 0:
                                log("FLOWSTATE == 0")
                                log(flow_info['flowState'])
                                aLink.update_flow(sender_id, "", 1)

                                aReply = QuickReply.QuickReply()
                                aReply.send_action_quick_reply(messaging_event["sender"]["id"])
                                break
                            
                            if flow_info['flowState'] == 1:
                                log("FLOWSTATE == 1")
                                if flow_info['flowType'] in "":
                                    log("FLOWSTATE == 1")
                                    aReply = QuickReply.QuickReply()
                                    aReply.send_action_quick_reply(messaging_event["sender"]["id"])
                                    break

                            #text based responses for split
                            #1, 3
                            if flow_info['flowType'] in "split":
                                if flow_info['flowState'] == 2:
                                    log("SPLIT CHECK NAME FLOWSTATE == 2")
                                    #check if the user entered a full name (first and last name)
                                    aName = message_text.split()
                                    if aName == 2:
                                        if flow_info['flowType'] in "":
                                            log("FLOWSTATE == 1")
                                            #send the buttons
                                            dbLink = DBLink.DBLink()
                                            the_users = dbLink.get_users_with_first_last_name(aName[0], aName[1])
                                            
                                            #if there are users in the db with that name
                                            if the_users is not None:
                                                aReply = QuickReply.QuickReply()
                                                aReply.send_users_quick_reply(sender_id, the_users)
                                                #increase flow number
                                                aLink.update_flow(sender_id, "split", 3)
                                            else:
                                                #let the user know that the person does not exist and to share the link
                                                someUser = UserInfo.UserInfo("",sender_id)
                                                anotherUser = UserInfo.UserInfo("","")
                                                
                                                #send share link message
                                                sendMsg = MsgBuilder.MessageBuilder(fromUser = someUser, toUser = anotherUser)
                                                sendMsg.send_share_link_message()
                                                
                                                #deletes the flow state row
                                                dbLink.delete_userID_state_info(sender_id)
                                                
                                                #reset flow state
                                                aLink.update_flow(sender_id, "", 1)
                                                break
                                    else:
                                        pass
                                        #resend the info for the state
                                        sendMsg.send_pay_who_message1()
                                        break
                                        
                                elif flow_info['flowState'] == 4:
                                    #get amount, check if its a number, if it is, increase flow,
                                    #if not send error message to re-enter amount
                                    anAmount = __getAmount__(message_text)
                                    
                                    #if the amount is valid, update state info
                                    # update flow
                                    # ask if what they entered is correct w/ confirm/deny QR buttons
                                    if anAmount is not None:
                                        aLink.update_flow(sender_id, "split", 5)
                                        #get flow state info
                                        tempInfo = aLink.get_state_info(sender_id)
                                        #update flow state info
                                        aLink.update_state_info_amount(sender_id, amount)
                                        #send QR confirm/deny buttons
                                        aReply = QuickReply.QuickReply()
                                        aReply.send_confirmDeny_quick_reply(sender_id)
                                    else:
                                        #re-enter information
                                        someUser = UserInfo.UserInfo("",sender_id)
                                        anotherUser = UserInfo.UserInfo("","")
                                        
                                        sendMsg = MsgBuilder.MessageBuilder(fromUser = someUser, toUser = anotherUser)
                                        sendMsg.send_error_try_again()
                                        sendMsg.send_enter_amount()
                                        break
                                    
                            if flow_info['flowType'] in "pay":
                                if flow_info['flowState'] == 2:
                                    
                                    #check name in db
                                    
                                    # dbLink = DBLink.DBLink()
                                    # the_user = dbLink.get_users_with_first_name(msgObj.getMessage())
                                    # the_payment.send_user_table(the_user)
                                    
                                    aLink.update_flow(sender_id, "pay", 3)
                                    sendMsg.send_which_user()
                                    break
                                
                                if flow_info['flowState'] == 3:
                                    aLink.update_flow(sender_id, "pay", 4)
                                    sendMsg.send_how_much_message()
                                    
                                if flow_info['flowState'] == 4: 
                                    m = re.search('\$(?!0\d)\d+(?:\.\d{2})?(?=\s|$)', msgObj.getMessage())
                                    if m:
                                        aLink.update_state_info_amount(sender_id, "", "-1", float(msgObj.amount))
                                        
                                        aLink.update_flow(sender_id, "pay", 5)
                                        
                                        aReply = QuickReply.QuickReply()
                                        aReply.send_confirmDeny_quick_reply(messaging_event["sender"]["id"])
                                        break  
                                        
                                    else:
                                        sendMsg.send_correct_amount_format_message()
                                        sendMsg.send_how_much_message()
                                        
                                        break    
                                    
                            if flow_info['flowType'] in "request":
                                
                                if flow_info['flowState'] == 2:
                                    aLink.update_flow(sender_id, "request", 3)
                                    sendMsg.send_which_user()
                                
                                if flow_info['flowState'] == 3:
                                    aLink.update_flow(sender_id, "request", 4)
                                    sendMsg.send_how_much_message()
                                    
                                if flow_info['flowState'] == 4: 
                                    m = re.search('\$(?!0\d)\d+(?:\.\d{2})?(?=\s|$)', msgObj.getMessage())
                                    if m:
                                        aLink.update_state_info_amount(sender_id, "", "-1", msgObj.amount)
                                        
                                        aLink.update_flow(sender_id, "request", 5)
                                        
                                        aReply = QuickReply.QuickReply()
                                        aReply.send_confirmDeny_quick_reply(messaging_event["sender"]["id"])
                                        break    
                                
                                    else:
                                        sendMsg.send_correct_amount_format_message()
                                        sendMsg.send_how_much_message()
                                        
                                        break 
                                                            
                        else:
    
                            payedUser = UserInfo.UserInfo("Unknown", messaging_event["sender"]["id"])
                            sendMsg = MsgBuilder.MessageBuilder(fromUser = payedUser, toUser = payedUser, messageType="simple", amount = str(msgObj.number))
                            

                            if(str(msgObj.number) == "-1"):
                                sendMsg.send_get_number_to_signup()
                            else:
                                request_info = GraphRequests.GraphRequests()
                                request_info.getUserInfo(messaging_event["sender"]["id"])
                                
                                sendMsg = MsgBuilder.MessageBuilder(fromUser = payedUser, toUser = payedUser, messageType="simple", amount = str(request_info.firstName))
                                aLink = DBLink.DBLink()
                                aLink.add_user(messaging_event["sender"]["id"], request_info.firstName, request_info.lastName, "unknown@gmail.com", request_info.profile_pic, str(msgObj.number))
                                sendMsg.send_signedup()
                                
                    except KeyError:
                        #anotherUser = UserInfo.UserInfo("", messaging_event["sender"]["id"])
                        aReply = QuickReply.QuickReply()
                        aReply.send_action_quick_reply(messaging_event["sender"]["id"])
                        
                        
                        
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    log("ENTERING POSTBACK")
                    something = messaging_event["sender"]
                    log(something)
                    for key in something:
                        value = something[key]
                        log("The key and value are ({}) = ({})".format(key, value))
    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    log("test2 {recipient}".format(recipient="derp"))

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
    
    #convert dict into json
    #####################################
    dataDict = {}
    dataDict['recipient'] = {}
    dataDict['message'] = {}
    
    dataDict['recipient']['id'] = str(recipient_id)
    dataDict['message']['text'] = str(message_text)
    
    data = json.dumps(dataDict)
    #######################################
    
    #send share button
    #########################################
    # dataDict = {}
    # dataDict['recipient'] = {}
    # dataDict['message'] = {}
    
    # dataDict['recipient']['id'] = str(recipient_id)
    # dataDict['message']['attachment'] = {}
    # dataDict['message']['attachment']['type'] =  "template"
    # dataDict['message']['attachment']['payload'] = {}
    # dataDict['message']['attachment']['payload']['template_type'] = "generic"
    # dataDict['message']['attachment']['payload']['elements'] = {}
    # dataDict['message']['attachment']['payload']['elements']['title'] = "teheee"
    # dataDict['message']['attachment']['payload']['elements']['subtitle'] = "ayeee"
    # dataDict['message']['attachment']['payload']['elements']['image_url'] = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    # dataDict['message']['attachment']['payload']['elements']['buttons'] = {}
    # dataDict['message']['attachment']['payload']['elements']['buttons']['type'] = "element_share"
    
    #data = json.dumps(dataDict)

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    
def getUserInfo(anId):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        str(anId)
    })
    r = requests.get("https://graph.facebook.com/v2.6/", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    else:
        log("SUCCESS  "+r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

"""
gets the amount from the string and determines if is a valid string or not
"""
def __getAmount__(data):
    # get words in string
    splits = data.split(" ")
    amount = "-1"
    # grab the word that has the $ char
    for word in splits:
        if '$' in word:
            # get number
            amount = word[1:]
            break
    try:
        amount = float(amount)
    except:
        amount = None

    return amount


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )