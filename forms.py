from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators = [DataRequired()])
#     password = PasswordField('Password', validators = [DataRequired()])
#     remember_me = BooleanField('Remember me')
#     submit = SubmitField('Login')