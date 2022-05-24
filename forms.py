from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, DateField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )
    
    

class TodoForm(FlaskForm):
    """Add todo form."""

    title = StringField(
        "Todo",
        validators=[InputRequired(), Length(max=100)],
    )
    complete = BooleanField(
        "Complete",
        validators=[InputRequired()],
    )
    dueDate = DateField("Due Date", format='%m/%d/%Y', validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
    

