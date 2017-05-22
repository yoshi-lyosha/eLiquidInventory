from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, StringField, PasswordField, FloatField, SelectField, SelectMultipleField, widgets, FieldList, FormField
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


class AddFlavoringToInvForm(AddFlavoringForm):
    amount = FloatField('Amount', [DataRequired()])


class AddNicotineForm(FlaskForm):
    producer_name = StringField('Producer', [DataRequired()])
    concentration = FloatField('Concentration', [DataRequired()])


class AddNicotineToInvForm(AddNicotineForm):
    amount = FloatField('Amount', [DataRequired()])


class EditNicotineForm(FlaskForm):
    amount = FloatField('Amount', [DataRequired()])


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddEliquidForm(FlaskForm):
    eliquid_name = StringField('Name', [DataRequired()])
    flavorings = MultiCheckboxField('Flavoring', coerce=int)
    # flavorings = FieldList(FormField(ManyForm), min_entries=1)
    amount = FloatField('Amount', [DataRequired()])
    status = SelectField('Status', choices=[('1', 'PUBLIC'), ('0', 'PRIVATE')])

    
class EliquidCraftForm(FlaskForm):
    quantity_of_pg = FloatField('PG', [DataRequired()])
    quantity_of_vg = FloatField('VG', [DataRequired()])
    # nicotine = BooleanField('Nicotine', [DataRequired()])
    # nicotine_base = SelectField('Nicotine Base', [DataRequired()], choices=[('pg', 'PG'), ('vg', 'VG')])
    # quantity_of_nicotine = FloatField('Nicotine', [DataRequired()])
    final_amount = FloatField('Amount', [DataRequired()])


class EliquidCreateForm(FlaskForm):
    eliquid_name = StringField('Name', [DataRequired()])
    status = SelectField('Status', choices=[('1', 'PUBLIC'), ('0', 'PRIVATE')])


class AddFlavoringForm(AddFlavoringForm):
    quantity = FloatField('Amount', [DataRequired()])
