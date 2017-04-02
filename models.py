import flask_sqlalchemy, app

#for heroku
app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
# app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

db = flask_sqlalchemy.SQLAlchemy(app.app)


class Users(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    user_id = db.Column(db.String(200))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(200))
    imgUrl = db.Column(db.String(300))
    phoneNumber = db.Column(db.String(20))

    def __init__(self, user_id, firstName, lastName, email, imgUrl, phoneNumber):
        
        self.user_id = user_id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.imgUrl = imgUrl
        self.phoneNumber = phoneNumber

    def __repr__(self):
        return '%s %s %s %s %s %s' % (self.user_id, self.firstName, self.lastName, self.email, self.imgUrl, self.phoneNumber)
        
class Friends(db.Model):
    __tablename__ = 'friends_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    user_id = db.Column(db.String(200))
    friend_id = db.Column(db.String(200))

    def __init__(self, user_id, friend_id):
        
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return '%s %s' % (self.user_id, self.friend_id)
        
class Pay(db.Model):
    __tablename__ = 'pay_table'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    owed_ID = db.Column(db.String(200))#requester
    pay_ID = db.Column(db.String(200))#requestee
    amount = db.Column(db.Float())
    time_stamp = db.Column(db.String(30))
    
    def __init__(self, owed_ID, pay_ID, amount, time_stamp):
    
        self.owed_ID = owed_ID
        self.pay_ID = pay_ID
        self.amount = amount
        self.time_stamp = time_stamp
        
    
    def __repr__(self):
        return '%s %s %f %s' % (self.owed_ID, self.pay_ID, self.amount, self.time_stamp)
        
class Payed(db.Model):
    __tablename__ = 'payed_table'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    payed_ID = db.Column(db.String(200))
    payee_ID = db.Column(db.String(200))
    amount = db.Column(db.Float)
    time_stamp = db.Column(db.String(30))
    
    def __init__(self, payed_ID, payee_ID, amount, time_stamp):
    
        self.payed_ID = payed_ID
        self.payee_ID = payee_ID
        self.amount = amount
        self.time_stamp = time_stamp
    
    def __repr__(self):
        return '%s %s %f %s' % (self.payed_ID, self.payee_ID, self.amount, self.time_stamp)

class StateInfo(db.Model):
    __tablename__ = 'state_info_table'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    senderID = db.Column(db.String(200))
    recipientID = db.Column(db.String(200))
    amount = db.Column(db.Float)
    flowType = db.Column(db.String(20))
    splitID = db.Column(db.String(20))
    time_stamp = db.Column(db.String(30))
    
    
    def __init__(self, senderID, recipientID, amount, flowType, splitID, time_stamp):
    
        self.senderID = senderID
        self.recipientID = recipientID
        self.amount = amount
        self.flowType = flowType
        self.splitID = splitID        
        self.time_stamp = time_stamp
    
    def __repr__(self):
        return '%s %s %f %s %s %s' % (self.senderID, self.recipientID, self.amount, self.flowType, self.splitID, self.time_stamp)

class FlowStates(db.Model):
    __tablename__ = 'flow_states_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    userID = db.Column(db.String(200))
    flowType = db.Column(db.String(20))
    flowState = db.Column(db.Integer)
    time_stamp = db.Column(db.String(30))

    def __init__(self, userID, flowType, flowState, time_stamp):
        
        self.userID = userID
        self.flowType = flowType
        self.flowState = flowState
        self.time_stamp = time_stamp
        
    def __repr__(self):
        return '%s %s %d %s' % (self.userID, self.flowType, self.flowState, self.time_stamp)