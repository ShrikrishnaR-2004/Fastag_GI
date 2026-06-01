from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, DecimalField,
    TextAreaField, SubmitField, DateField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Regexp,
    NumberRange, ValidationError, Optional
)

INDIAN_STATES = [
    ('', '— Select State —'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra & Nagar Haveli and Daman & Diu'),
    ('Delhi', 'Delhi (NCT)'),
    ('Jammu and Kashmir', 'Jammu & Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]


class AddVehicleForm(FlaskForm):
    registration_number = StringField(
        'Registration Number',
        validators=[
            DataRequired(message='Registration number is required.'),
            Length(min=4, max=20, message='Enter a valid registration number.'),
            Regexp(
                r'^[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{4}$',
                message='Enter a valid Indian registration number (e.g. TN XX AB 1234).'
            )
        ]
    )
    vehicle_type = SelectField(
        'Vehicle Type',
        choices=[
            ('Car', 'Car / SUV'),
            ('Truck', 'Truck / HCV'),
            ('Bus', 'Bus'),
            ('LCV', 'Light Commercial Vehicle'),
            ('Two-Wheeler', 'Two-Wheeler'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register Vehicle')


class RechargeForm(FlaskForm):
    amount = DecimalField(
        'Recharge Amount (₹)',
        places=2,
        validators=[
            DataRequired(message='Please enter an amount.'),
            NumberRange(min=100, max=50000, message='Amount must be between ₹100 and ₹50,000.')
        ]
    )
    payment_mode = SelectField(
        'Payment Mode',
        choices=[
            ('UPI', 'UPI (Google Pay, PhonePe, Paytm)'),
            ('Debit Card', 'Debit Card'),
            ('Credit Card', 'Credit Card'),
            ('Net Banking', 'Net Banking'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Recharge Wallet')


class UpdateProfileForm(FlaskForm):
    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Full name is required.'),
            Length(min=3, max=100)
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.'),
            Length(max=120)
        ]
    )
    mobile_number = StringField(
        'Mobile Number',
        validators=[
            DataRequired(),
            Regexp(r'^\d{10}$', message='Enter a valid 10-digit mobile number.')
        ]
    )
    submit = SubmitField('Save Changes')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired(message='Current password is required.')]
    )
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters.'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Password must contain uppercase, lowercase, and a number.'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords do not match.')
        ]
    )
    submit = SubmitField('Update Password')


class KYCForm(FlaskForm):
    # Section 1: Personal Information
    full_name = StringField(
        'Full Name (as per ID)',
        validators=[DataRequired(), Length(min=3, max=100)]
    )
    date_of_birth = DateField(
        'Date of Birth',
        validators=[DataRequired(message='Date of birth is required.')],
        format='%Y-%m-%d'
    )
    gender = SelectField(
        'Gender',
        choices=[('', '-- Select --'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        validators=[DataRequired(message='Please select your gender.')]
    )
    nationality = StringField(
        'Nationality',
        validators=[DataRequired(), Length(max=50)],
        default='Indian'
    )

    # Section 2: Identity Proof
    id_type = SelectField(
        'ID Proof Type',
        choices=[
            ('', '-- Select --'),
            ('Aadhaar', 'Aadhaar Card'),
            ('PAN', 'PAN Card'),
            ('Passport', 'Passport'),
            ('Driving License', 'Driving License'),
            ('Voter ID', 'Voter ID / EPIC Card'),
        ],
        validators=[DataRequired(message='Please select an ID proof type.')]
    )
    id_number = StringField(
        'ID Number',
        validators=[DataRequired(), Length(min=4, max=30)]
    )

    # Section 3: Address Details
    address_line1 = StringField(
        'Address Line 1',
        validators=[DataRequired(), Length(max=150)]
    )
    address_line2 = StringField(
        'Address Line 2 (Optional)',
        validators=[Optional(), Length(max=150)]
    )
    city = StringField(
        'City / District',
        validators=[DataRequired(), Length(max=60)]
    )
    state = SelectField(
        'State / UT',
        choices=INDIAN_STATES,
        validators=[DataRequired(message='Please select your state.')]
    )
    pin_code = StringField(
        'PIN Code',
        validators=[
            DataRequired(),
            Regexp(r'^\d{6}$', message='Enter a valid 6-digit PIN code.')
        ]
    )
    country = StringField(
        'Country',
        validators=[DataRequired(), Length(max=50)],
        default='India'
    )

    submit = SubmitField('Submit KYC for Verification')
