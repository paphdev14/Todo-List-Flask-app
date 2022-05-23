from crypt import methods
import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import false
from models import connect_db, db, User
from forms import UserForm

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.route("/")
def home_page():
    '''
    Home page
    Redirect to TODO lists
    '''
    return render_template('index.html')

#=================== Todo Routes ===================#
@app.route('/todos')
def show_todos():
    return render_template('todos.html')







#=================== User Routes ===================#

# Register
@app.route('/signup', methods=['GET', 'POST'])
def register_user():
    ''''
    To register users and add them to db
    '''
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.sign_up(username, password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome! Successfully Created Your Account!')
        return redirect('/todos')
    return render_template('register.html', form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    For users login
    '''
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.authenticate(username, password)
        if existing_user:
            return redirect('/todos')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

 

'''
To allow update/refresh static files to flask server 
'''
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values) 

# if __name__ == "__main__":
#     app.run(port=3000)
