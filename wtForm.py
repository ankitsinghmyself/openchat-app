from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

class RegistartionForm(FlaskForm):
    """Registration form"""

    username = StringField('username_lable', validators=[InputRequired(message="Input Required"),
    Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    password = PasswordField('password_lable', validators=[InputRequired(message="Password Required"),
    Length(min=6, max=25, message="Password must be between 6 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password Required"),
    EqualTo('password', message="Password Must Match")])

    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists, Select a diffrent Username.")