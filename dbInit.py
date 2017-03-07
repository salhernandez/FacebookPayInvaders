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
new_user = models.Users("Joshua Smith", "josmith@csumb.edu", "nope.png")
models.db.session.add(new_user)


new_user = models.Users("Salvador Hernandez", "salvhernandez@csumb.edu", "nope.png")
models.db.session.add(new_user)


new_user = models.Users("Anna Pomelov", "apomelovz@csumb.edu", "nope.png")
models.db.session.add(new_user)

models.db.session.commit()