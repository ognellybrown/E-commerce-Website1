

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from market.routes import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length (min=2, max=20)])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password1 = PasswordField('password', validators=[DataRequired(), Length(min=4)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Already exits, Please use a different username.')

    def validate_email_address(self, email):
        user = User.query.filter_by(email_address=email.data).first()
        if user is not None:
            raise ValidationError('Email Already exits, Please use a different email address.') 


class Loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PurchaseItemform(FlaskForm):
    submit = SubmitField('Purchase Item!')

class SellItemform(FlaskForm):
    submit = SubmitField('Sell Item!')
