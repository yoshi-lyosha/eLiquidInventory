from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    # remember_me = BooleanField('remember_me', default=False)


class RegisterForm(FlaskForm):
    user_name = StringField('Username', [DataRequired()])
    email = StringField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Repeat Password', [
      DataRequired(),
      EqualTo('password', message='Passwords must match')
      ])
    # accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    # re_captcha = RecaptchaField()


class AddFlavoringForm(FlaskForm):
    flavoring_name = StringField('Flavoring', [DataRequired()])
    producer_name = StringField('Producer', [DataRequired()])
    amount = FloatField('Amount', [DataRequired()])
