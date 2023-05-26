from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.fields import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from package.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    Username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired()])
    Confirm_Password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("Password")])
    Submit = SubmitField("Sign Up")

    def validate_Username(self, Username):
        user = User.query.filter_by(username=Username.data).first()
        if user:
            raise ValidationError("This username is taken. Please choose a different one.")

    def validate_Email(self, Email):
        user = User.query.filter_by(email=Email.data).first()
        if user:
            raise ValidationError("This email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("remember me")
    Submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    Username = StringField("Username", validators=[DataRequired()])
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    Submit = SubmitField("Update")

    def validate_Username(self, Username):
        if current_user.username != Username.data:
            user = User.query.filter_by(username=Username.data).first()
            if user:
                raise ValidationError("This Username is taken. Please choose a different one.")

    def validate_Email(self, Email):
        if current_user.email != Email.data:
            user = User.query.filter_by(email=Email.data).first()
            if user:
                raise ValidationError("This Email is taken. Please choose a different one.")


class Requestresetform(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Submit = SubmitField("request ")

    def validate_Email(self, Email):
        user = User.query.filter_by(email=Email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")


class Resetpasswordform(FlaskForm):
    Password = PasswordField("Password", validators=[DataRequired()])
    Confirm_Password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("Password")])
    Submit = SubmitField("Reset Password")
