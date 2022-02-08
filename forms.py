from email.policy import default
from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, Length


class AddPetForm(FlaskForm):
    """Form to add new pet"""
    name = StringField("Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[
                          ("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[
                       Optional(), NumberRange(min=0, max=30)])
    notes = StringField("Notes", validators=[Optional(), Length(min=10)])
    available = BooleanField("Available", default=True)


class EditPetForm(FlaskForm):
    """Form to edit information of the pet"""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional(), Length(min=10)])
    available = BooleanField("Available")
