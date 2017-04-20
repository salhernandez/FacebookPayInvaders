import flask_sqlalchemy, app, sys, time, re


from sqlalchemy import or_, and_

#for heroku
app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
#app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

import models
db = flask_sqlalchemy.SQLAlchemy(app.app)

class DBLink(object):
    def __init__(self):
        pass
    
    """
    ===USERS TABLE METHODS
    ============================================================================
    """
    
    """
    Adds a user to the Users table in the DB
    Converts the first, and last name and email into all lowercase for easier
    db lookup
    """
    def add_user(self, userID, firstName, lastName, email, imageURL, phoneNumber):
        ts = int(time.time())
        
        #sanitize input
        #convert first name, last name, and email to lowercase
        firstName = firstName.lower()
        lastName = lastName.lower()
        email = email.lower()
        
        # first is the person who is OWED, second is the person that needs to pay
        signup_request = models.Users(userID, firstName, lastName, email, imageURL, phoneNumber)
        models.db.session.add(signup_request)
        models.db.session.commit()
    
    """
    Checks if a user is in the db
    Return rows that match, otherwise it returns None
    
    
    aLink = DBLink.DBLink()
    a = aLink.get_user_in_db("985245348244242")
    log(a['firstName'])
    """
    def get_user_in_db(self, userID):
        userInDB = models.Users.query.filter_by(user_id=str(userID)).all()
        
        #ID was found
        if userInDB is not None:
            userDict = {}
        
            for row in userInDB:
                userDict['userID'] = row.user_id
                userDict['firstName'] = row.firstName
                userDict['lastName'] = row.lastName
                userDict['email'] = row.email
                userDict['imgUrl'] = row.imgUrl
                userDict['phoneNumber'] = row.phoneNumber
                break
            return userDict
        else:
            return None
    """
    Gets all the users in the database
    
    
    """
    def get_all_user_in_db(self):
        userInDB = models.Users.query.all()
        
        #ID was found
        if userInDB is not None:
           
            # print userInDB
            userInDBDict = {}
            
            count = 0
            for row in userInDB:
                # print row.owed_ID
                userInDBDict[count] = {}
                userInDBDict[count]['userID'] = row.user_id
                userInDBDict[count]['firstName'] = row.firstName
                userInDBDict[count]['lastName'] = row.lastName
                userInDBDict[count]['email'] = row.email
                userInDBDict[count]['imgUrl'] = row.imgUrl
                userInDBDict[count]['phoneNumber'] = row.phoneNumber
                
                count = count + 1
            return userInDBDict
                
        else:
            return None
    """
    Gets all the users in the db based on the first name
    Returns users that match the first name
    
    make note of the number iterator that starts at 0
    
    aLink = DBLink.DBLink()
    a = aLink.get_users_with_first_name("sal")
    log(a[0][USER_ID_IS_HERE]['firstName'])
    """
    def get_users_with_first_name(self, first_name):
        first_name = first_name.lower()
        userInDB = models.Users.query.filter(models.Users.firstName.startswith(first_name)).all()
        
        if userInDB is not None:
            
            # print userInDB
            userInDBDict = {}
            
            count = 0
            for row in userInDB:
                # print row.owed_ID
                userInDBDict[count] = {}
                userInDBDict[count][row.user_id] = {}
                userInDBDict[count][row.user_id]['userID'] = row.user_id
                userInDBDict[count][row.user_id]['firstName'] = row.firstName
                userInDBDict[count][row.user_id]['lastName'] = row.lastName
                userInDBDict[count][row.user_id]['email'] = row.email
                userInDBDict[count][row.user_id]['imgUrl'] = row.imgUrl
                userInDBDict[count][row.user_id]['phoneNumber'] = row.phoneNumber
                
                count = count + 1
            return userInDBDict
        else:
            return None
    
    """
    Gets all the users in the db based on the last name
    Returns users that match the last name
    
    make note of the number iterator that starts at 0
    
    aLink = DBLink.DBLink()
    a = aLink.get_users_with_last_name("he")
    log(a[0][userID]['firstName'])
    return "test"
    """
    def get_users_with_last_name(self, last_name):
        last_name = last_name.lower()
        userInDB = models.Users.query.filter(models.Users.lastName.startswith(last_name)).all()
        
        if userInDB is not None:
            # print userInDB
            userInDBDict = {}
            
            count = 0
            for row in userInDB:
                # print row.owed_ID
                userInDBDict[count] = {}
                userInDBDict[count][row.user_id] = {}
                userInDBDict[count][row.user_id]['userID'] = row.user_id
                userInDBDict[count][row.user_id]['firstName'] = row.firstName
                userInDBDict[count][row.user_id]['lastName'] = row.lastName
                userInDBDict[count][row.user_id]['email'] = row.email
                userInDBDict[count][row.user_id]['imgUrl'] = row.imgUrl
                userInDBDict[count][row.user_id]['phoneNumber'] = row.phoneNumber
                
                count = count + 1
            return userInDBDict
        else:
            return None
    
    """
    Gets all the users in the db based on first and last name
    Returns users that match the last name
    
    make note of the number iterator that starts at 0
    
    aLink = DBLink.DBLink()
    a = aLink.get_users_with_first_last_name("anna", "pomelov")
    log(a[0][userID]['firstName'])
    return "test"
    
    """
    def get_users_with_first_last_name(self, first_name, last_name):
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        userInDB = models.Users.query.filter_by(firstName=first_name , lastName=last_name).all()
        
        if userInDB is not None:
            userInDBDict = {}
            
            count = 0
            for row in userInDB:
                # print row.owed_ID
                userInDBDict[count] = {}
                userInDBDict[count][row.user_id] = {}
                userInDBDict[count][row.user_id]['userID'] = row.user_id
                userInDBDict[count][row.user_id]['firstName'] = row.firstName
                userInDBDict[count][row.user_id]['lastName'] = row.lastName
                userInDBDict[count][row.user_id]['email'] = row.email
                userInDBDict[count][row.user_id]['imgUrl'] = row.imgUrl
                userInDBDict[count][row.user_id]['phoneNumber'] = row.phoneNumber
                
                count = count + 1
            return userInDBDict
        else:
            return None
            
    """
    Updates the email of the user based on the ID
    """
    def update_user_email(self, uID, new_email):
        uID = str(uID)
        new_email = new_email.lower()
        
        checkEmail = self.is_email_valid(new_email)
        
        if checkEmail is True:
            admin = models.Users.query.filter_by(user_id=uID).update(dict(email=new_email))
            models.db.session.commit()
            return True
        elif checkEmail is False:
            return False
        
    """
    Updates the phone number of the user based on the ID
    """
    def update_user_phone(self, uID, new_phone):
        uID = str(uID)
        new_phone = str(new_phone)
        
        aFlag = self.is_number_tryexcept(new_phone)
        
        if aFlag is False:
            return False
        
        elif aFlag is True:
            admin = models.Users.query.filter_by(user_id=uID).update(dict(phoneNumber=new_phone))
            models.db.session.commit()
        
    """
    ===END USERS TABLE METHODS
    ============================================================================
    """
    
    """
    ===FRIENDS TABLE METHODS
    ============================================================================
    """
    
    """
    Gets the friends of the user
    Returns a list of users that are friends with the submitted ID
    """
    def get_friends_of_user(self, userID):
        friendsInDB = models.Friends.query.filter(or_(models.Friends.user_id == userID, models.Friends.friend_id == userID)).all()
        
        uniqueFriends = []
        
        #ID was found
        if friendsInDB is not None:
            for row in friendsInDB:
                a = str(row.user_id)
                b = str(row.friend_id)
                
                if a != userID:
                    uniqueFriends.append(a)
                    continue
                if b != userID:
                    uniqueFriends.append(b)
                    continue
                
            return uniqueFriends 
        else:
            return None
    
    """
    Checks if user 1 is friends with user 2
    Returns False, if the user is not in the system
    or if they are not friends
    """
    def are_they_friends(self, user_id_1, user_id_2):
        friends = self.get_friends_of_user(user_id_1)
        
        aFlag = False
        
        for friend in friends:
            if friend == user_id_2:
                aFlag = True
                break
        
        return aFlag
    
    """
    Sets friends
    """
    def set_friends(self, user_id_1, user_id_2):
        user_id_1 = str(user_id_1)
        user_id_2 = str(user_id_2)
        
        #Friends
        add_friendship = models.Friends(user_id_1, user_id_2)
        models.db.session.add(add_friendship)
        models.db.session.commit()
        
    """
    ===END FRIENDS TABLE METHODS
    ============================================================================
    """
    
    
    """
    ===PAYED(PAID) TABLE METHODS
    ============================================================================
    """
    
    """
    Adds a payment to the Payed table
    """
    def add_payment(self, toID, fromID, amount):
        ts = int(time.time())
        #first ID is the person who got PAYED, second is PAYEE
        payment = models.Payed(toID, fromID, float(amount), ts)
        models.db.session.add(payment)
        models.db.session.commit()
    
    """
    Gets all transactions where the user was paid TO
    Returns a dictionary with paid to id, amount, and time stamp
    """
    def get_all_paid_to(self, userID):
        
        paidToRecords = models.Payed.query.filter_by(payed_ID=str(userID)).all()
        
        # print userInDB
        paidToDict = {}
        
        if paidToRecords is not None:
            count = 0
            for row in paidToRecords:
                # print row.owed_ID
                paidToDict[count] = {}
                paidToDict[count][row.payee_ID] = {}
                paidToDict[count][row.payee_ID]['amount'] = row.amount
                paidToDict[count][row.payee_ID]['timestamp'] = row.time_stamp
                
                count = count + 1
            return paidToDict
        else:
            return None
    """
    Get all the payments made by a user
    Returns a dictionary of ids, amount, and time stamp
    of users paid
    """
    def get_all_paid_from(self, userID):
        
        paymentsMadeRecords = models.Payed.query.filter_by(payee_ID=str(userID)).all()
        
        if paymentsMadeRecords is not None:
            # print userInDB
            paymentsMadeDict = {}
            
            count = 0
            for row in paymentsMadeRecords:
                # print row.owed_ID
                paymentsMadeDict[count] = {}
                paymentsMadeDict[count][row.payed_ID] = {}
                paymentsMadeDict[count][row.payed_ID]['amount'] = row.amount
                paymentsMadeDict[count][row.payed_ID]['timestamp'] = row.time_stamp
                
                count = count + 1
            return paymentsMadeDict
        else:
            return None
    
    """
    ===END PAYED(PAID) TABLE METHODS
    ============================================================================
    """
    
    """
    ===PAY TABLE METHODS
    ============================================================================
    """
    
    """
    Adds a payment request to the pay table
    """
    def add_request(self, requesterID, requesteeID, amount):
        ts = int(time.time())
        # first is the person who is OWED, second is the person that needs to pay
        pay_request = models.Pay(requesterID, requesteeID, amount, ts)
        models.db.session.add(pay_request)
        models.db.session.commit()
    """
    Gets amounts owed BY the user
    Returns a dictionary with the id the user owes to, amount, and timestamp
    """
    def get_all_owed_by(self, userID):
        
        owedRecords = models.Pay.query.filter_by(pay_ID=str(userID)).all()
        
        if owedRecords is not None:
            # print userInDB
            owedDict = {}
            
            count = 0
            for row in owedRecords:
                # print row.owed_ID
                owedDict[count] = {}
                owedDict[count][row.owed_ID] = {}
                owedDict[count][row.owed_ID]['amount'] = row.amount
                owedDict[count][row.owed_ID]['timestamp'] = row.time_stamp
                
                count = count + 1
            return owedDict
        else:
            return None
    
    """
    Gets amounts owed TO the user
    Returns a dictionary with the id the user owed by, amount, and timestamp
    """
    def get_all_owed_to(self, userID):
        
        owedToRecords = models.Pay.query.filter_by(owed_ID=str(userID)).all()
        
        if owedToRecords is not None:
            owedToDict = {}
            
            count = 0
            for row in owedToRecords:
                # print row.owed_ID
                
                owedToDict[count] = {}
                owedToDict[count][row.pay_ID] = {}
                owedToDict[count][row.pay_ID]['amount'] = row.amount
                owedToDict[count][row.pay_ID]['timestamp'] = row.time_stamp
                
                count = count + 1
            
            return owedToDict
        else:
            return None
        
    """
    delete_pay_request
    Deletes the pay request from the db
    Uses the payeeID, and timestamp
    """
    def delete_pay_request(self, payeeID, the_ts):
        the_ts = str(the_ts)
        record = models.Pay.query.filter(and_(models.Pay.pay_ID == payeeID, models.Pay.time_stamp == the_ts)).first()
        PayInfoDict = {}
        
        if record is not None:
            PayInfoDict['owed_ID'] = record.owed_ID
            PayInfoDict['pay_ID'] = record.pay_ID
            PayInfoDict['amount'] = record.amount
            PayInfoDict['timestamp'] = record.time_stamp
        
        models.db.session.delete(record)        
        models.db.session.commit()
        return PayInfoDict
        
    """
    ===END PAY TABLE METHODS
    ============================================================================
    """
    
    """
    ===STATE INFO TABLE METHODS
    ============================================================================
    """
    
    """
    Sets a state info row, method should be used when the user initiates a new flow,
    if there is no splitID, please init to "-1"
    
    TO INIT A FLOW
    CHANGE THE FIRST FIELD TO THE ID OF THE USER WITH THE FLOW
    the rest will be filled with the update methods
    
    aLink = DBLink.DBLink()
    aLink.set_state_info("1204927079622878","",0.0,"request", "-1")
    """
    def set_state_info(self, senderID, recipientID, amount, flowType, splitID = "-1"):
        #StateInfo
        senderID = str(senderID)
        recipientID = str(recipientID)
        ts = str(int(time.time()))
        flowType = flowType.lower()
        
        newStateInfo = models.StateInfo(senderID, recipientID, amount, flowType, splitID, ts)
        models.db.session.add(newStateInfo)
        
        models.db.session.commit()
    
    """
    Gets the state information based on the person who started the flow
    Returns all the info from the row ONLY 1 ROW
    """
    def get_state_info(self, userID):
        
        stateInfoRecords = models.StateInfo.query.filter_by(senderID=str(userID)).first()
        stateInfoDict = {}
        
        if stateInfoRecords is not None:
            
            # print row.owed_ID
            stateInfoDict['recipientID'] = stateInfoRecords.recipientID
            stateInfoDict['amount'] = stateInfoRecords.amount
            stateInfoDict['flowType'] = stateInfoRecords.flowType
            stateInfoDict['splitID'] = stateInfoRecords.splitID
            stateInfoDict['timestamp'] = stateInfoRecords.time_stamp
                
            return stateInfoDict
        
        else:
            return None
    
    """
    Updates the recipient based on the senderID, new recipient id, and split id (even if its "-1")
    """
    def update_state_info_recipient_ID(self, sender_id, recipient_id, split_id = "-1"):
        sender_id = str(sender_id)
        recipient_id = str(recipient_id)
        split_id = str(split_id)
        
        admin = models.StateInfo.query.filter(and_(models.StateInfo.senderID==sender_id, models.StateInfo.recipientID=="", models.StateInfo.splitID == split_id)).update(dict(recipientID=recipient_id))
        models.db.session.commit()
    
    """
    Updates the amount based on sender id, recipient id, and split id (even if its -1)
    """
    def update_state_info_amount(self, sender_id, recipient_id, split_id, new_amount):
        sender_id = str(sender_id)
        recipient_id = str(recipient_id)
        split_id = str(split_id)
        
        admin = models.StateInfo.query.filter(and_(models.StateInfo.senderID==sender_id, models.StateInfo.recipientID==recipient_id, models.StateInfo.splitID == split_id)).update(dict(amount=new_amount))
        models.db.session.commit()
    
    """
    Gets a user state info table started
    pass in the userID and the flowType
    dbLink.init_state_info("1596606567017003", "split")
    """
    def init_state_info(self, senderID, flowType):
        splitID = "-1"
        recipientID=""
        amount= 0.0
        
        senderID = str(senderID)
        recipientID = str(recipientID)
        ts = str(int(time.time()))
        flowType = flowType.lower()
        
        newStateInfo = models.StateInfo(senderID, recipientID, amount, flowType, splitID, ts)
        models.db.session.add(newStateInfo)
        
        models.db.session.commit()
    """
    ===END STATE INFO TABLE METHODS
    ============================================================================
    """
    
    """
    ===FLOW STATE TABLE METHODS
    ============================================================================
    """
    
    """
    This method is to be called when the user cannot be found in the flow states
    table, thus initializing a row for the user
    """
    def init_flow_state(self, userID):
        #StateInfo
        userID = str(userID)
        
        ts = str(int(time.time()))
        
        newFlowState = models.FlowStates(userID, "", 0, ts)
        models.db.session.add(newFlowState)
        
        models.db.session.commit()
    
    """
    Used to updated flow type and flow status
    """
    def update_flow(self, user_id, flow_type, flow_status):
        #StateInfo
        user_id = str(user_id)
        flow_type = flow_type.lower()
        
        aFlag = self.is_number_tryexcept(flow_status)
        
        if aFlag is True:
            ts = str(int(time.time()))
            flow_status = int(flow_status)
            
            models.FlowStates.query.filter_by(userID=user_id).update(dict(flowType=flow_type, flowState=flow_status))
            models.db.session.commit()
    
    """
    Gets the flow state for the user ID
    
    aLink = DBLink.DBLink()
    flow_info = aLink.get_flow_state("985245348244242")
    log(flow_info['userID'])
    """
    def get_flow_state(self, user_id):
        user_id = str(user_id)
        
        flowInfo = models.FlowStates.query.filter_by(userID=user_id).all()
        flowInfoDict = {}
        
        if flowInfo is not None:
            for row in flowInfo:
                flowInfoDict['userID'] = row.userID
                flowInfoDict['flowType'] = row.flowType
                flowInfoDict['flowState'] = row.flowState
                flowInfoDict['timestamp'] = row.time_stamp
            
            #print flowInfoDict
            return flowInfoDict
        else:
            return None
    """
    ===END FLOW STATE TABLE METHODS
    ============================================================================
    """
    
    """
    checks if the string is a number
    """
    def is_number_tryexcept(self, s):
        """ Returns True is string is a number. """
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    """
    Simple wrapper for logging to stdout on heroku
    """
    def log(self, text):
        print str(text)
        sys.stdout.flush()
    
    """
    checks the email with regex
    """
    def is_email_valid(self, email): 
        match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
        if match:
            return True
        else:
            return False
    
    """
    perform_payment_transaction
    
    aLink = DBLink.DBLink()
    
    a = aLink.perform_payment_transaction("1596606567017003", 1491129978)
    """
    def perform_payment_transaction(self, payeeID, time_stamp):
        #delete payment from db
        deletedInfo = self.delete_pay_request(payeeID, time_stamp)
        #add it to the payed(paid) table
        self.add_payment(deletedInfo['owed_ID'], deletedInfo['pay_ID'], deletedInfo['amount'])
        
        
    """
    Displays the instance variables of the object
    """
    def __str__(self):
        return str(self.__dict__)