from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

def invalid_credentials(form, field):
    """ username and password checker """
    username_entered = form.username.data
    password_entered = field.data
    
    #check credentials are valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Username or password is incorrect")


class RegistartionForm(FlaskForm):
    """Registration form"""

    username = StringField('username_lable', validators=[InputRequired(message="Input Required"),
    Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    password = PasswordField('password_lable', validators=[InputRequired(message="Password Required"),
    Length(min=6, max=25, message="Password must be between 6 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password Required"),
    EqualTo('password', message="Password Must Match")])

    submit_button = SubmitField('Create')
    
    #inline custom validater
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists, Select a diffrent Username.")

class LoginForm(FlaskForm):
    """login form """
    username = StringField('username_lable', validators=[InputRequired(message="Input Required")])
    password = StringField('password_lable', validators=[InputRequired(message="Input Required"), invalid_credentials])
    submit_button = SubmitField('Login')