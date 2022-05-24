import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''
    db.app = app
    db.init_app(app)
    
    
class ToDO(db.Model):
    
    '''Create TODO DB'''
    
    __tablename__ = 'todos'
    
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.String(100))
    
    complete = db.Column(db.Boolean)
    
    dueDate = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow()
    )
    username = db.Column(   
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )    


class User(db.Model):
    '''
    Create user profile DB
    '''
    __tablename__ = 'users'
    
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    

    @classmethod
    def sign_up(cls, username, pwd, first_name, last_name):
        '''Register user w/hashed password & return user'''
        
        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        user_info = cls(username=username, password = hashed_utf8, first_name=first_name, last_name=last_name)
        # return instance of user w/username and hashed pwd
        # db.session.add(user_info)
        return user_info

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
        



    
    































# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)