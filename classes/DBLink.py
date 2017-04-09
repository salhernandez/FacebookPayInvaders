import flask_sqlalchemy, app, sys, time, re
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
    """
    def get_user_in_db(self, userID):
        userInDB = models.Users.query.filter_by(user_id=str(userID)).all()
        
        #ID was found
        if userInDB is not None:
            return userInDB
        else:
            return None
    
    """
    Gets all the users in the db based on the first name
    Returns users that match the first name
    """
    def get_users_with_first_name(self, first_name):
        first_name = first_name.lower()
        userInDB = models.Users.query.filter(models.Users.firstName.startswith(first_name)).all()
        
        if userInDB is not None:
            return userInDB
        else:
            return None
    
    """
    Gets all the users in the db based on the last name
    Returns users that match the last name
    """
    def get_users_with_last_name(self, last_name):
        last_name = last_name.lower()
        userInDB = models.Users.query.filter(models.Users.lastName.startswith(last_name)).all()
        
        if userInDB is not None:
            return userInDB
        else:
            return None
    
    """
    Gets all the users in the db based on first and last name
    Returns users that match the last name
    """
    def get_users_with_first_last_name(self, first_name, last_name):
        first_name = first_name.lower()
        last_name = last_name.lower()
        
        userInDB = models.Users.query.filter_by(firstName=first_name , lastName=last_name).all()
        
        if userInDB is not None:
            return userInDB
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
    ===END PAY TABLE METHODS
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
            self.log("bad phone")
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
    Displays the instance variables of the object
    """
    def __str__(self):
        return str(self.__dict__)