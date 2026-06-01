import os
from app import create_app
from app.extensions import db
from app.models import User, Vehicle, Transaction
from datetime import datetime, timedelta, timezone
import random
import sys

app = create_app(os.getenv('FLASK_ENV', 'default'))

with app.app_context():
    delete_only = False
    target = None
    for arg in sys.argv[1:]:
        if arg.lower() in ('delete', 'clear', '--delete', '-d'):
            delete_only = True
        else:
            target = arg

    if target:
        user = User.query.filter(
            (User.email == target) | (User.mobile_number == target)
        ).first()
        if not user:
            print(f"User with email/mobile '{target}' not found!")
            exit()
    else:
        user = User.query.first()
        if not user:
            print("No users found in the database. Please register a user through the UI first.")
            exit()
        print("No specific user provided. Defaulting to the first user.")

    if delete_only:
        print(f"Deleting seed data for user: {user.email}")
        Transaction.query.filter_by(user_id=user.id).delete()
        Vehicle.query.filter_by(user_id=user.id).delete()
        user.wallet_balance = 0.0
        db.session.commit()
        print("Data deleted successfully!")
        exit()
        
    print(f"Seeding data for user: {user.email}")
    
    # 1. Update wallet balance
    user.wallet_balance = 2450.00
    
    # 2. Add vehicles (clear old ones first)
    Transaction.query.filter_by(user_id=user.id).delete()
    Vehicle.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    
    # Make registration numbers unique per user to prevent IntegrityError
    reg1 = f"TN 12 AB {user.id:04d}"
    reg2 = f"TN 14 XY {9000 + user.id:04d}"
    v1 = Vehicle(user_id=user.id, registration_number=reg1, is_active=True)
    v2 = Vehicle(user_id=user.id, registration_number=reg2, is_active=True)
    db.session.add_all([v1, v2])
    db.session.commit()
    
    # 3. Add transactions
    now = datetime.now(timezone.utc)
    
    # Recharge
    t1 = Transaction(
        user_id=user.id, type='recharge', amount=1000.0, location='UPI / Paytm', status='success',
        created_at=now - timedelta(days=5)
    )
    
    # Tolls
    t2 = Transaction(
        user_id=user.id, vehicle_id=v1.id, type='toll', amount=-110.0, location='Khed Shivapur Toll Plaza', status='success',
        created_at=now - timedelta(days=2)
    )
    t3 = Transaction(
        user_id=user.id, vehicle_id=v1.id, type='toll', amount=-140.0, location='Talegaon Toll Plaza', status='success',
        created_at=now - timedelta(days=4)
    )
    t4 = Transaction(
        user_id=user.id, vehicle_id=v2.id, type='toll', amount=-45.0, location='Vashi Toll Naka', status='success',
        created_at=now - timedelta(days=10)
    )
    t5 = Transaction(
        user_id=user.id, vehicle_id=v2.id, type='toll', amount=-85.0, location='Bandra Worli Sea Link', status='success',
        created_at=now - timedelta(days=12)
    )
    t6 = Transaction(
        user_id=user.id, vehicle_id=v1.id, type='parking', amount=-150.0, location='Phoenix Mall Parking', status='success',
        created_at=now - timedelta(days=3)
    )
    
    db.session.add_all([t1, t2, t3, t4, t5, t6])
    db.session.commit()
    
    print("Database seeded successfully with vehicles and transactions!")
