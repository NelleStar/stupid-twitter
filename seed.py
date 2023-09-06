from app import app
from models import db, User, Tweet
from flask_bcrypt import Bcrypt

db.drop_all()
db.create_all()

bcrypt = Bcrypt()

u1 = User(username="userOne", 
          password=bcrypt.generate_password_hash("passOne").decode("utf-8"), )
u2 = User(username="userTwo", 
          password=bcrypt.generate_password_hash("passTwo").decode("utf-8"),  )
u3 = User(username="userThree", 
          password=bcrypt.generate_password_hash("passThree").decode("utf-8"), )

db.session.add_all([u1, u2, u3])
db.session.commit()

 