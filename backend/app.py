from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_cors import CORS

# Import our models
from models.models import db, User, UserProfile, Stakeholder, Program, Recommendation, NoticeBoard, Admin

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

# Import and register routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.stakeholder_routes import stakeholder_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(stakeholder_bp)

# Basic home route
@app.route('/')
def home():
    """Landing page route"""
    try:
        return render_template('home.html')
    except:
        # Fallback if template doesn't exist
        return "Welcome to the Poverty Line Project!"

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)