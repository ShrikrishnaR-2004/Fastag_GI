from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, SignupForm, ForgotPasswordForm
from app.models import User
from app.extensions import db


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = SignupForm()
    if form.validate_on_submit():
        email  = form.email.data.strip().lower()
        mobile = form.mobile_number.data.strip()

        # ── Explicit duplicate checks (belt-and-suspenders on top of form validators) ──
        existing_email  = User.query.filter_by(email=email).first()
        existing_mobile = User.query.filter_by(mobile_number=mobile).first()

        if existing_email:
            form.email.errors.append('This email address is already registered. Please sign in instead.')
        if existing_mobile:
            form.mobile_number.errors.append('This mobile number is already linked to an account.')
        if existing_email or existing_mobile:
            return render_template('auth/signup.html', title='Create Account', form=form)

        # ── Safe to create ──
        try:
            user = User(
                full_name=form.full_name.data.strip(),
                email=email,
                mobile_number=mobile,
                is_active=True,
                email_verified=False,
                role='Customer'
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! You can now sign in.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError:
            db.session.rollback()
            # Identify which constraint was violated
            existing_email  = User.query.filter_by(email=email).first()
            existing_mobile = User.query.filter_by(mobile_number=mobile).first()
            if existing_email:
                form.email.errors.append('This email address is already registered.')
            if existing_mobile:
                form.mobile_number.errors.append('This mobile number is already linked to an account.')
            if not existing_email and not existing_mobile:
                flash('A duplicate entry error occurred. Please check your details and try again.', 'danger')

    return render_template('auth/signup.html', title='Create Account', form=form)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        login_val = form.login_id.data.strip()
        user = User.query.filter(
            (User.email == login_val) | (User.mobile_number == login_val)
        ).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email / mobile or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Your account has been suspended. Contact support.', 'warning')
            return redirect(url_for('auth.login'))

        # Update last login timestamp
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        login_val = form.login_id.data.strip()
        user = User.query.filter(
            (User.email == login_val) | (User.mobile_number == login_val)
        ).first()
        
        # Always show success message to prevent enumeration
        flash('If an account with that email/mobile exists, a password reset link has been sent.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/forgot_password.html', title='Forgot Password', form=form)
