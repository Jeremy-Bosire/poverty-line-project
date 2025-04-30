from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_cors import CORS

# Import our models
from models import db, User, UserProfile, Stakeholder, Program, Recommendation, NoticeBoard, Admin

# This sets up the app and loads the configuration for our database.
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configuration settings
app.config['SECRET_KEY'] = '860161b45d69b1c3a46aef53a0342eabd737bbcf997812f6252a3759defc084b'
# Use PostgreSQL for production, SQLite for development
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:empty@localhost:5432/povertyline'
# Uncomment below for SQLite during development if needed
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

# Initialize the extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

@app.route('/')
def home():
    """Landing page route"""
    try:
        return render_template('home.html')
    except:
        # Fallback if template doesn't exist
        return "Welcome to the Poverty Line Project!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    from forms import RegistrationForm  # Import here to avoid circular imports
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
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    from forms import LoginForm  # Import here to avoid circular imports
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

@app.route('/logout', methods=['GET'])
def logout():
    """User logout route"""
    logout_user()
    return redirect('http://localhost:5000')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """User account management route"""
    from forms import UpdateAccountForm  # Import here to avoid circular imports
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

@app.route('/add_user_profile', methods=['POST'])
@login_required
def add_user_profile():
    """Add user profile information"""
    data = request.get_json()

    # Check if user already has a profile
    existing_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    if existing_profile:
        # Update existing profile
        existing_profile.gender = data.get('gender')
        existing_profile.location = data.get('location')
        existing_profile.age = data.get('age')
        existing_profile.skills = ",".join(data.get('skills', []))  # Turn skills array into a string
        existing_profile.employment_status = data.get('employment_status')
        existing_profile.education = data.get('education')
        existing_profile.profile_completed = True
        db.session.commit()
        message = "Profile updated successfully!"
    else:
        # Create a new profile
        new_user_profile = UserProfile(
            user_id=current_user.id,
            gender=data.get('gender'),
            location=data.get('location'),
            age=data.get('age'),
            skills=",".join(data.get('skills', [])),
            employment_status=data.get('employment_status'),
            education=data.get('education'),
            profile_completed=True
        )
        db.session.add(new_user_profile)
        db.session.commit()
        message = "Profile created successfully!"

    return jsonify({"message": message}), 201

@app.route('/get_organization_data')
@login_required
def get_organization_data():
    """Get user profile data for organizations"""
    # Only allow stakeholders or admins to access this data
    if current_user.role not in ['org', 'admin']:
        return jsonify({"error": "Unauthorized access"}), 403
        
    users = db.session.query(User, UserProfile).join(UserProfile, User.id == UserProfile.user_id).all()

    result = []
    for user, profile in users:
        result.append({
            'username': user.username,
            'email': user.email,
            'gender': profile.gender,
            'location': profile.location,
            'age': profile.age,
            'skills': profile.skills,
            'employment_status': profile.employment_status,
            'education': profile.education,
            'poverty_risk_score': user.poverty_risk_score
        })
    return jsonify({"profiles": result})

# API routes for recommendations and programs can be added here

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)