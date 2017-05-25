from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, StringField, PasswordField, FloatField, SelectField, SelectMultipleField, widgets, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
    # remember_me = BooleanField('remember_me', default=False)


class RegisterForm(FlaskForm):
    user_name = StringField('Username', [DataRequired()])
    email = StringField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Repeat Password', [
      DataRequired(),
      EqualTo('password', message='Passwords must match')
      ])
    submit = SubmitField('Register')
    # accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    # re_captcha = RecaptchaField()


class AddFlavoringForm(FlaskForm):
    flavoring_name = StringField('Flavoring', [DataRequired()])
    producer_name = StringField('Producer', [DataRequired()])
    submit = SubmitField('Add flavoring')


class AddFlavoringToInvForm(AddFlavoringForm):
    amount = FloatField('Amount', [DataRequired()])
    submit = SubmitField('Add')


class AddNicotineForm(FlaskForm):
    producer_name = StringField('Producer', [DataRequired()])
    concentration = FloatField('Concentration', [DataRequired()])
    submit = SubmitField('Add')


class AddNicotineToInvForm(AddNicotineForm):
    amount = FloatField('Amount', [DataRequired()])
    submit = SubmitField('Add')

class EditNicotineForm(FlaskForm):
    amount = FloatField('Amount', [DataRequired()])


class EliquidCraftForm(FlaskForm):
    quantity_of_pg = FloatField('PG', [DataRequired()])
    quantity_of_vg = FloatField('VG', [DataRequired()])
    # nicotine = BooleanField('Nicotine', [DataRequired()])
    # nicotine_base = SelectField('Nicotine Base', [DataRequired()], choices=[('pg', 'PG'), ('vg', 'VG')])
    # quantity_of_nicotine = FloatField('Nicotine', [DataRequired()])
    final_amount = FloatField('Amount', [DataRequired()])
    submit = SubmitField("Craft it!")


class EliquidCreateForm(FlaskForm):
    eliquid_name = StringField('Name', [DataRequired()])
    status = SelectField('Status', choices=[('1', 'PUBLIC'), ('0', 'PRIVATE')])
    submit = SubmitField("Add eLiquid")


class AddFlavoringToEliquidForm(FlaskForm):
    flavoring_name = StringField('Flavoring', [DataRequired()])
    producer_name = StringField('Producer', [DataRequired()])
    quantity = FloatField('Amount', [DataRequired()])
    submit = SubmitField("Add flavoring")
