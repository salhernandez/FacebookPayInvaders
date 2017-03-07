import flask_sqlalchemy, app

#for heroku
app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
db = flask_sqlalchemy.SQLAlchemy(app.app)


class Users(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    name = db.Column(db.String(120))
    email = db.Column(db.String(200))
    imgUrl = db.Column(db.String(120))

    def __init__(self, name, email, imgUrl):
        
        self.name = name
        self.email = email
        self.imgUrl = imgUrl

    def __repr__(self):
        return '%s %s %s' % (self.name, self.email, self.imgUrl)
        
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
    owed_ID = db.Column(db.String(200))
    pay_ID = db.Column(db.String(200))
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
