from flask_wtf import FlaskForm
from sqlalchemy.sql.functions import current_user
from wtforms.fields import EmailField, PasswordField, StringField, DecimalField, FileField, SelectField, BooleanField, DateTimeLocalField, FloatField, SubmitField
from wtforms.validators import InputRequired, DataRequired, NumberRange, Length, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from flask_bcrypt import bcrypt
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView



from app.extensions import db, login_manager


class UserDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), unique=True, nullable=False)
    lname = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(9), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.String(1), nullable=False, default="0")

    @property
    def __repr__(self):
        return f"<UserDB: {self.userID}, {self.email}, {self.password}, {self.access_level}, {self.fname}, {self.lname}, {self.postcode}, {self.address}>"



class SignupForm(FlaskForm):
    email = EmailField("Email:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    fname = StringField("First Name:", validators=[InputRequired()])
    lname = StringField("First Name:", validators=[InputRequired()])
    postcode = StringField("Postcode:", validators=[InputRequired()])
    address = StringField("Address:", validators=[InputRequired()])

class LoginForm(FlaskForm):
    name = StringField("Email:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password',validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6characters.")])
    confirm_password = PasswordField('Confirm New Password',validators=[DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Change Password')