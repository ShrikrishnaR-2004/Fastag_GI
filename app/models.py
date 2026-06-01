from datetime import datetime, timezone
from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.extensions import db, login_manager

ph = PasswordHasher()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, index=True, nullable=False)
    mobile_number = db.Column(db.String(15),  unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20),  default='Customer', nullable=False)
    is_active     = db.Column(db.Boolean,     default=True,  nullable=False)
    email_verified = db.Column(db.Boolean,    default=False, nullable=False)
    wallet_balance = db.Column(db.Float,      default=0.0,   nullable=False)
    created_at    = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))
    last_login    = db.Column(db.DateTime,    nullable=True)
    
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password: str):
        self.password_hash = ph.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

    def __repr__(self):
        return f'<User {self.email}>'

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_number = db.Column(db.String(20), unique=True, index=True, nullable=False)
    vehicle_type = db.Column(db.String(30), default='Car', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = db.relationship('Transaction', backref='vehicle', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True) # Nullable for recharges
    type = db.Column(db.String(20), nullable=False) # 'toll', 'parking', 'fuel', 'recharge'
    amount = db.Column(db.Float, nullable=False) # Positive for recharge, negative for toll/parking/fuel
    location = db.Column(db.String(100), nullable=True) # Toll Plaza name or payment gateway name
    status = db.Column(db.String(20), default='success', nullable=False) # 'success', 'pending', 'failed'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class KYC(db.Model):
    __tablename__ = 'kyc'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Personal info
    full_name    = db.Column(db.String(100), nullable=True)
    date_of_birth= db.Column(db.Date,       nullable=True)
    gender       = db.Column(db.String(10),  nullable=True)
    nationality  = db.Column(db.String(50),  default='Indian', nullable=True)

    # Identity proof
    id_type      = db.Column(db.String(30),  nullable=True)   # Aadhaar / PAN / Passport / DL / Voter ID
    id_number    = db.Column(db.String(30),  nullable=True)

    # Address
    address_line1= db.Column(db.String(150), nullable=True)
    address_line2= db.Column(db.String(150), nullable=True)
    city         = db.Column(db.String(60),  nullable=True)
    state        = db.Column(db.String(60),  nullable=True)
    pin_code     = db.Column(db.String(10),  nullable=True)
    country      = db.Column(db.String(50),  default='India',  nullable=True)

    # Status
    # 'not_submitted' | 'pending' | 'verified' | 'rejected'
    status       = db.Column(db.String(20),  default='not_submitted', nullable=False)
    submitted_at = db.Column(db.DateTime,    nullable=True)
    verified_at  = db.Column(db.DateTime,    nullable=True)
    remarks      = db.Column(db.String(255), nullable=True)  # rejection reason / admin note

    user         = db.relationship('User', backref=db.backref('kyc', uselist=False))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
