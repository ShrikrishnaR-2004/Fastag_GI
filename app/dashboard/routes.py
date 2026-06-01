from datetime import datetime, timezone, timedelta
import calendar

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func

from app.dashboard import bp
from app.dashboard.forms import AddVehicleForm, RechargeForm, UpdateProfileForm, ChangePasswordForm, KYCForm
from app.extensions import db
from app.models import Vehicle, Transaction, User, KYC


# ─── helpers ──────────────────────────────────────────────────────────────────
def _now():
    return datetime.now(timezone.utc)


def _sidebar_context():
    """Data needed by every page's sidebar."""
    active_vehicles_count = Vehicle.query.filter_by(
        user_id=current_user.id, is_active=True).count()
    kyc = KYC.query.filter_by(user_id=current_user.id).first()
    kyc_status = kyc.status if kyc else 'not_submitted'
    return dict(active_vehicles_count=active_vehicles_count, kyc_status=kyc_status)


# ─── Overview (existing route kept here for blueprint) ────────────────────────
@bp.route('/')
@login_required
def overview():
    now = _now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    wallet_balance = current_user.wallet_balance

    vehicles = Vehicle.query.filter_by(user_id=current_user.id)\
        .order_by(Vehicle.created_at.desc()).all()
    active_vehicles_count = sum(1 for v in vehicles if v.is_active)

    tolls_paid_this_month = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'toll',
        Transaction.status == 'success',
        Transaction.created_at >= start_of_month
    ).scalar() or 0.0
    tolls_paid_this_month = abs(tolls_paid_this_month)

    last_recharge = Transaction.query.filter_by(
        user_id=current_user.id, type='recharge', status='success'
    ).order_by(Transaction.created_at.desc()).first()

    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.created_at.desc()).limit(8).all()

    expenses = db.session.query(Transaction.type, func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type.in_(['toll', 'parking', 'fuel']),
        Transaction.status == 'success',
        Transaction.created_at >= start_of_month
    ).group_by(Transaction.type).all()
    expense_data = {'toll': 0, 'parking': 0, 'fuel': 0}
    for type_, amount in expenses:
        expense_data[type_] = round(abs(amount), 2)

    monthly_labels, monthly_values = [], []
    for i in range(5, -1, -1):
        target = now - timedelta(days=i * 30)
        ms = datetime(target.year, target.month, 1, tzinfo=timezone.utc)
        me = datetime(target.year + 1, 1, 1, tzinfo=timezone.utc) if target.month == 12 \
            else datetime(target.year, target.month + 1, 1, tzinfo=timezone.utc)
        total = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type.in_(['toll', 'parking', 'fuel']),
            Transaction.status == 'success',
            Transaction.created_at >= ms,
            Transaction.created_at < me
        ).scalar() or 0.0
        monthly_labels.append(calendar.month_abbr[target.month])
        monthly_values.append(round(abs(total), 2))

    total_spent = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type.in_(['toll', 'parking', 'fuel']),
        Transaction.status == 'success'
    ).scalar() or 0.0
    total_spent = round(abs(total_spent), 2)

    return render_template('dashboard/dashboard.html',
                           wallet_balance=wallet_balance,
                           active_vehicles_count=active_vehicles_count,
                           vehicles=vehicles,
                           tolls_paid_this_month=tolls_paid_this_month,
                           last_recharge=last_recharge,
                           recent_transactions=recent_transactions,
                           expense_data=expense_data,
                           monthly_labels=monthly_labels,
                           monthly_values=monthly_values,
                           total_spent=total_spent,
                           now=now)


# ─── My Vehicles ─────────────────────────────────────────────────────────────
@bp.route('/vehicles', methods=['GET', 'POST'])
@login_required
def vehicles():
    form = AddVehicleForm()
    if form.validate_on_submit():
        reg = form.registration_number.data.strip().upper().replace(' ', ' ')
        existing = Vehicle.query.filter_by(registration_number=reg).first()
        if existing:
            flash('This vehicle is already registered in the system.', 'danger')
        else:
            v = Vehicle(
                user_id=current_user.id,
                registration_number=reg,
                vehicle_type=form.vehicle_type.data,
                is_active=True
            )
            db.session.add(v)
            db.session.commit()
            flash(f'Vehicle {reg} registered successfully!', 'success')
            return redirect(url_for('dash.vehicles'))

    user_vehicles = Vehicle.query.filter_by(user_id=current_user.id)\
        .order_by(Vehicle.created_at.desc()).all()

    ctx = _sidebar_context()
    return render_template('dashboard/vehicles.html',
                           form=form,
                           user_vehicles=user_vehicles,
                           now=_now(), **ctx)


@bp.route('/vehicles/<int:vehicle_id>/toggle', methods=['POST'])
@login_required
def toggle_vehicle(vehicle_id):
    v = Vehicle.query.filter_by(id=vehicle_id, user_id=current_user.id).first_or_404()
    v.is_active = not v.is_active
    db.session.commit()
    state = 'activated' if v.is_active else 'deactivated'
    flash(f'Vehicle {v.registration_number} {state}.', 'success')
    return redirect(url_for('dash.vehicles'))


# ─── Recharge Wallet ─────────────────────────────────────────────────────────
@bp.route('/recharge', methods=['GET', 'POST'])
@login_required
def recharge():
    form = RechargeForm()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        current_user.wallet_balance += amount
        tx = Transaction(
            user_id=current_user.id,
            type='recharge',
            amount=amount,
            location=f'Recharge via {form.payment_mode.data}',
            status='success'
        )
        db.session.add(tx)
        db.session.commit()
        flash(f'₹{amount:,.2f} added to your wallet successfully!', 'success')
        return redirect(url_for('dash.recharge'))

    ctx = _sidebar_context()
    return render_template('dashboard/recharge.html',
                           form=form,
                           wallet_balance=current_user.wallet_balance,
                           now=_now(), **ctx)


# ─── All Transactions ─────────────────────────────────────────────────────────
@bp.route('/transactions')
@login_required
def transactions():
    type_filter   = request.args.get('type', '')
    status_filter = request.args.get('status', '')
    page          = request.args.get('page', 1, type=int)

    q = Transaction.query.filter_by(user_id=current_user.id)
    if type_filter:
        q = q.filter(Transaction.type == type_filter)
    if status_filter:
        q = q.filter(Transaction.status == status_filter)

    pagination = q.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False
    )

    ctx = _sidebar_context()
    return render_template('dashboard/transactions.html',
                           pagination=pagination,
                           transactions=pagination.items,
                           type_filter=type_filter,
                           status_filter=status_filter,
                           now=_now(), **ctx)


# ─── Profile Settings ────────────────────────────────────────────────────────
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form  = UpdateProfileForm(obj=current_user, prefix='profile')
    password_form = ChangePasswordForm(prefix='pwd')

    if profile_form.validate_on_submit() and 'profile-submit' in request.form:
        new_email  = profile_form.email.data.strip().lower()
        new_mobile = profile_form.mobile_number.data.strip()

        email_taken  = User.query.filter(User.email == new_email,         User.id != current_user.id).first()
        mobile_taken = User.query.filter(User.mobile_number == new_mobile, User.id != current_user.id).first()

        if email_taken:
            profile_form.email.errors.append('This email is already used by another account.')
        elif mobile_taken:
            profile_form.mobile_number.errors.append('This mobile number is already used by another account.')
        else:
            current_user.full_name     = profile_form.full_name.data.strip()
            current_user.email         = new_email
            current_user.mobile_number = new_mobile
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('dash.profile'))

    if password_form.validate_on_submit() and 'pwd-submit' in request.form:
        if not current_user.check_password(password_form.current_password.data):
            password_form.current_password.errors.append('Current password is incorrect.')
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dash.profile'))

    ctx = _sidebar_context()
    return render_template('dashboard/profile.html',
                           profile_form=profile_form,
                           password_form=password_form,
                           now=_now(), **ctx)


# ─── KYC Update ──────────────────────────────────────────────────────────────
@bp.route('/kyc', methods=['GET', 'POST'])
@login_required
def kyc():
    record = KYC.query.filter_by(user_id=current_user.id).first()
    form   = KYCForm(obj=record)

    # Pre-fill name from user profile if KYC is new
    if request.method == 'GET' and record is None:
        form.full_name.data = current_user.full_name

    if form.validate_on_submit():
        if record is None:
            record = KYC(user_id=current_user.id)
            db.session.add(record)

        # Block edits once verified
        if record.status == 'verified':
            flash('Your KYC is already verified and cannot be modified.', 'warning')
            return redirect(url_for('dash.kyc'))

        record.full_name     = form.full_name.data.strip()
        record.date_of_birth = form.date_of_birth.data
        record.gender        = form.gender.data
        record.nationality   = form.nationality.data.strip()
        record.id_type       = form.id_type.data
        record.id_number     = form.id_number.data.strip().upper()
        record.address_line1 = form.address_line1.data.strip()
        record.address_line2 = form.address_line2.data.strip() if form.address_line2.data else ''
        record.city          = form.city.data.strip()
        record.state         = form.state.data
        record.pin_code      = form.pin_code.data.strip()
        record.country       = form.country.data.strip()
        record.status        = 'pending'
        record.submitted_at  = _now()
        db.session.commit()
        flash('KYC details submitted successfully! Verification usually takes 24–48 hours.', 'success')
        return redirect(url_for('dash.kyc'))

    ctx = _sidebar_context()
    return render_template('dashboard/kyc.html',
                           form=form,
                           record=record,
                           now=_now(), **ctx)
