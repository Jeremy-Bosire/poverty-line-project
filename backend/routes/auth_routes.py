from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from models.models import db, User
from forms.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_pw, 
            role=form.account_type.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            session['user_id'] = user.id
            # Check the user's role and redirect accordingly
            if user.role == 'user':
                return redirect('http://localhost:5173/userpage')  # Redirect to user-specific page
            elif user.role == 'org':
                return redirect('http://localhost:5173/organisationpage')  # Redirect to organization-specific page
            else:
                return redirect('http://localhost:5173')  # Default landing page if role doesn't match
        else:
            flash('Login unsuccessful. Check your email and password.', 'danger')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """User logout route"""
    logout_user()
    return redirect('http://localhost:5000')

@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """User account management route"""
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info updated')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)