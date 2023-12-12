from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    the_key = StringField("The Key",
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    username = StringField("Username",
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField("Confirm Password",
                             validators=[
                                 DataRequired(),
                                 EqualTo("password")
                             ])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_duplicate_user = User.query.filter_by(username=username.data).first()
        if existing_duplicate_user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        existing_duplicate_user = User.query.filter_by(email=email.data).first()
        if existing_duplicate_user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    picture = FileField("Update Profile Picture",
                        validators=[
                            FileAllowed(["jpg", "png", "svg"])
                        ])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            existing_duplicate_user = User.query.filter_by(username=username.data).first()
            if existing_duplicate_user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            existing_duplicate_user = User.query.filter_by(email=email.data).first()
            if existing_duplicate_user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    submit = SubmitField("Request Password Request")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register an account first.')

class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField("Confirm Password",
                             validators=[
                                 DataRequired(),
                                 EqualTo("password")
                             ])
    submit = SubmitField("Request Password")