import time
import models

import flask_sqlalchemy, app

#app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

db = flask_sqlalchemy.SQLAlchemy(app.app)

ts = time.time()
ts = str(int(ts))

#Pay
ts = str(int(time.time()))
payment = models.Pay("985245348244242", "1596606567017003", 15.99, ts)
models.db.session.add(payment)
models.db.session.commit()

#Payed
ts = str(int(time.time()))
payment = models.Payed("985245348244242", "1596606567017003", 15.99, ts)
models.db.session.add(payment)
models.db.session.commit()

#Friends
add_friendship = models.Friends("985245348244242", "1596606567017003")
models.db.session.add(add_friendship)
models.db.session.commit()

#Users
new_user = models.Users("985245348244242", "joshua", "smith", "josmith@csumb.edu", "nope.png", "8314285108")
models.db.session.add(new_user)


new_user = models.Users("1596606567017003","salvador", "hernandez", "salvhernandez@csumb.edu", "nope.png", "6197345766")
models.db.session.add(new_user)


new_user = models.Users("1204927079622878", "anna", "pomelov", "apomelov@csumb.edu", "nope.png", "4152839158")
models.db.session.add(new_user)

#StateInfo
ts = str(int(time.time()))
newStateInfo = models.StateInfo("985245348244242", "1204927079622878", 88.88, "pay","-1", ts)
models.db.session.add(newStateInfo)

ts = str(int(time.time()))
newStateInfo = models.StateInfo("985245348244242", "1204927079622878", 77.77, "request","-1", ts)
models.db.session.add(newStateInfo)

ts = str(int(time.time()))
newStateInfo = models.StateInfo("1204927079622878", "985245348244242", 55.55, "pay","99", ts)
models.db.session.add(newStateInfo)

#FlowStates
ts = str(int(time.time()))
newFlowStateInfo = models.FlowStates("985245348244242", "split", 1, ts)
models.db.session.add(newFlowStateInfo)

ts = str(int(time.time()))
newFlowStateInfo = models.FlowStates("1204927079622878", "pay", 2, ts)
models.db.session.add(newFlowStateInfo)

ts = str(int(time.time()))
newFlowStateInfo = models.FlowStates("1596606567017003", "request", 1, ts)
models.db.session.add(newFlowStateInfo)

models.db.session.commit()