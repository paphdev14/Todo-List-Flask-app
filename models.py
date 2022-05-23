import re
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''
    db.app = app
    db.init_app(app)
    
    
class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)
    
    password = db.Column(db.Text, unique=True)

    @classmethod
    def sign_up(cls, username, pwd):
        '''Register user w/hashed password & return user'''
        
        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        # return instance of user w/username and hashed pwd
        return cls(username=username, password = hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        '''
        validate if user exists and password is correct
        Return user if valid; else return false
        '''
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        

# class ToDO(db.Model):
#     pass































# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)