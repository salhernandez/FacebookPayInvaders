from app import db
from sqlalchemy.dialects.postgresql import JSON

class Users(db.Model):
    __tablename__ = 'users_info'

    id = db.Column(db.Integer, primary_key=True)  # key
    name = db.Column(db.String(120))
    email = db.Column(db.String(200))
    imgUrl = db.Column(db.String(120))

    def __init__(self, name, email, imgUrl):
        
        self.name = name
        self.email = email
        self.imgUrl = imgUrl

    def __repr__(self):
        return '<MessageTable text: %s %s %s>' % self.name % self.email % self.imgUrl
        
class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)  # key
    user_id = db.Column(db.String(120))
    friend_id = db.Column(db.String(200))

    def __init__(self, user_id, friend_id):
        
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return '<MessageTable text: %d %d %s>' % self.user_id % self.friend_id
        
class Pay(db.Model):
    __tablename__ = 'pay'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    owed_ID = db.Column(db.Integer)
    pay_ID = db.Column(db.Integer)
    amount = db.Column(db.Float())
    
    def __init__(self, owed_ID, pay_ID, amount):
    
        self.owed_ID = owed_ID
        self.pay_ID = pay_ID
        self.amount = amount
    
    def __repr__(self):
        return '<Pay double: %d %d %f>' % self.owed_ID % self.pay_ID % self.amount
        
class Payed(db.Model):
    __tablename__ = 'payed'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    payed_ID = db.Column(db.Integer)
    payee_ID = db.Column(db.Integer)
    amount = db.Column(db.Float)
    
    def __init__(self, owed_ID, pay_ID, amount):
    
        self.pay_ID = owed_ID
        self.payee_ID = pay_ID
        self.amount = amount
    
    def __repr__(self):
        return '<Pay double: %d %d %f>' % self.pay_ID % self.payee_ID % self.amount
