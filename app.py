import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import false
from models import connect_db, db, User, ToDO
from forms import LoginForm, RegisterForm, DeleteForm, TodoForm
from werkzeug.exceptions import Unauthorized

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todo_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
# db.drop_all()
db.create_all()

#=================== Root Routes ===================#
@app.route('/')
def home_page():
    '''
    Home page
    Registration
    '''
    return redirect('/signup')

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('todos/404.html'), 404

#=================== User Routes ===================#

'''Register'''
@app.route('/signup', methods=['GET', 'POST'])
def register_user():
    ''''
    To register users and handle form submission
    '''
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.sign_up(username, password, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        
        session['username'] = user.username
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f"/users/{user.username}")
    else:
        return render_template('users/register.html', form=form)


''''Login'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    For users login
    '''
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)       
        if user:
            flash(f"Welcome Back, {user.first_name}!")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password']
            return render_template("users/login.html", form=form)

    return render_template('users/login.html', form=form)

# Logout
@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

# Handle User accounts
@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

#=================== Todos Routes ===================#

@app.route("/users/<username>/todo/new", methods=["GET", "POST"])
def new_todo(username):
    """Show add-todo form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        complete = form.complete.data
        due_date = form.dueDate.data

        todo = ToDO(
            title=title,
            content=complete,
            due_date = due_date,
            username=username,
        )

        db.session.add(todo)
        db.session.commit()

        return redirect(f"/users/{todo.username}")

    else:
        return render_template("todos/new.html", form=form)


# Edit Todos
@app.route("/todo/<int:todo_id>/update", methods=["GET", "POST"])
def update_todo(todo_id):
    """Show update-todo form and process it."""

    todo = ToDO.query.get(todo_id)

    if "username" not in session or todo.username != session['username']:
        raise Unauthorized()

    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        title = form.title.data
        complete = form.complete.data
        due_date = form.dueDate.data

        db.session.commit()

        return redirect(f"/users/{todo.username}")

    return render_template("/todo/edit.html", form=form, todo=todo)

# Delete
@app.route("/todo/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    """Delete todo."""

    todo = ToDO.query.get(todo_id)
    if "username" not in session or todo.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(todo)
        db.session.commit()

    return redirect(f"/users/{todo.username}")













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
