from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TelField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Regexp, ValidationError
)
from app.models import User


class LoginForm(FlaskForm):
    login_id    = StringField(
        'Email or Mobile Number',
        validators=[DataRequired(message='Please enter your email or mobile number.'),
                    Length(min=5, max=120)]
    )
    password    = PasswordField(
        'Password',
        validators=[DataRequired(message='Please enter your password.')]
    )
    remember_me = BooleanField('Keep me signed in')
    submit      = SubmitField('Sign In')


class SignupForm(FlaskForm):
    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Full name is required.'),
            Length(min=3, max=100, message='Name must be between 3–100 characters.')
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Email address is required.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120)
        ]
    )
    mobile_number = TelField(
        'Mobile Number',
        validators=[
            DataRequired(message='Mobile number is required.'),
            Regexp(r'^\d{10}$', message='Enter a valid 10-digit mobile number.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=8, message='Password must be at least 8 characters.'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Password must contain uppercase, lowercase, and a number.'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords do not match.')
        ]
    )
    accept_terms = BooleanField(
        'Accept Terms',
        validators=[DataRequired(message='You must accept the Terms & Conditions.')]
    )
    submit = SubmitField('Create Account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError(
                'An account with this email already exists. '
                'Try signing in, or use a different email address.'
            )

    def validate_mobile_number(self, field):
        if User.query.filter_by(mobile_number=field.data.strip()).first():
            raise ValidationError(
                'This mobile number is already linked to an account. '
                'Try signing in, or use a different number.'
            )

class ForgotPasswordForm(FlaskForm):
    login_id = StringField(
        'Email or Mobile Number',
        validators=[DataRequired(message='Please enter your email or mobile number.'),
                    Length(min=5, max=120)]
    )
    submit = SubmitField('Reset Password')

