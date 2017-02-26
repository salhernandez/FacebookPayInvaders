from app import db
from sqlalchemy.dialects.postgresql import JSON


class AllAccount(db.Model):
    __tablename__ = 'all_accounts'

    id = db.Column(db.Integer, primary_key=True)  # key
    message = db.Column(JSON)

    def __init__(self, message):
        
        self.message = message

    def __repr__(self):
        return '{}'.format(self.message)

class GroupAccounts(db.Model):
    __tablename__ = 'group_accounts'

    id = db.Column(db.Integer, primary_key=True)  # key
    message = db.Column(JSON)

    def __init__(self, message):
        
        self.message = message

    def __repr__(self):
        return '{}'.format(self.message)
        
class SingleAccounts(db.Model):
    __tablename__ = 'single_accounts'

    id = db.Column(db.Integer, primary_key=True)  # key
    message = db.Column(JSON)

    def __init__(self, message):
        
        self.message = message

    def __repr__(self):
        return '{}'.format(self.message)