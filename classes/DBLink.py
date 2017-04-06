import flask_sqlalchemy, app, sys, time

#for heroku
app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
#app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

import models
db = flask_sqlalchemy.SQLAlchemy(app.app)

class DBLink(object):
    def __init__(self):
        pass
    
    #amount needs to be a float
    def add_payment(self, toID, fromID, amount):
        ts = int(time.time())
        #first ID is the person who got PAYED, second is PAYEE
        payment = models.Payed(toID, fromID, float(amount), ts)
        models.db.session.add(payment)
        models.db.session.commit()
    
    def add_request(self, requesterID, requesteeID, amount):
        ts = int(time.time())
        # first is the person who is OWED, second is the person that needs to pay
        pay_request = models.Pay(requesterID, requesteeID, amount, ts)
        models.db.session.add(pay_request)
        models.db.session.commit()
    
    def add_user(self, userID, firstName, lastName, email, imageURL, phoneNumber):
        ts = int(time.time())
        # first is the person who is OWED, second is the person that needs to pay
        signup_request = models.Users(userID, firstName, lastName, email, imageURL, phoneNumber)
        models.db.session.add(signup_request)
        models.db.session.commit()
        
    def log(self, text):  # simple wrapper for __log__ging to stdout on heroku
        print str(text)
        sys.stdout.flush()

    def __str__(self):
        return str(self.__dict__)