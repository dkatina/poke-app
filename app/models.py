from app import db, login
from flask_login import UserMixin #Specific to User Class model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self): #Talks to machine
        return f'< User: {self.email} | {self.id}>'

    def __str__(self): #Talks to machine
        return f'< User: {self.email} | {self.first_name} {self.first_name}>'

        #returns a more secure version of our password
    def hash_pass(self, my_password):
        return generate_password_hash(my_password)
        
        #On login, if email bares fruit reach into that user's data and see if they're stored hashed password = this password thats been hashed
    def check_pass(self, login_pass):
        return check_password_hash(self.password, login_pass)
        
    def save(self):
        db.session.add(self) #adds the user to the session
        db.session.commit() #saves the user's info to the database

    #when registering a new user the form produces a dictionary, this function unpacks that dictionary into our database table
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.icon = data['icon']
        self.password = self.hash_pass(data['password'])   #takes whatever password they gave, hashes it, and stores it 

    def get_icon_url(self):
        return f"http://avatars.dicebear.com/api/croodles/{self.icon}.svg"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
