# This file defines all the database models used in the Poverty Line Project.
# We're using Flask-SQLAlchemy to interact with a PostgreSQL database.

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# This is our main database object. We'll initialize it inside app.py.
db = SQLAlchemy()

# Users will provide demographic info, which will help us generate insights and recommendations.
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique
    image_file = db.Column(db.String(28), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)  # Password will be hashed
    role = db.Column(db.String(20), default='user')

    # Profile fields moved to UserProfile with a relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)
    
    # Risk score predicted by the ML model (e.g., 0.82 = high risk)
    poverty_risk_score = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many relationship: a user can have multiple recommendations
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)

    # One-to-many relationship: a user can post multiple local insights
    knowledge_posts = db.relationship('NoticeBoard', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Extended user profile information
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Basic demographic fields used for analysis and ML recommendations
    gender = db.Column(db.String(10))
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)
    education = db.Column(db.String(100))
    employment_status = db.Column(db.String(20))
    skills = db.Column(db.String(500))
    
    # Whether the user has completed their profile or not
    profile_completed = db.Column(db.Boolean, default=False)


# Represents NGOs or organizations that want to assist users (e.g., by posting jobs or training programs).
class Stakeholder(db.Model):
    __tablename__ = 'stakeholders'

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Whether this stakeholder has been approved by an admin
    approved = db.Column(db.Boolean, default=False)

    # Region they operate in (used for filtering/searching)
    region = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many relationship: an org can offer multiple programs
    programs = db.relationship('Program', backref='stakeholder', lazy=True)


# These are support offerings (jobs, scholarships, training, etc.) posted by stakeholders.
class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)  # Name/title of the program
    description = db.Column(db.Text)  # Long description of what the program is
    type = db.Column(db.String(50))  # What type of program (job, training, etc.)
    eligibility = db.Column(db.String(250))  # Short eligibility requirements
    location = db.Column(db.String(100))  # Where the program is located

    # Foreign key to stakeholder who created this program
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholders.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Stores ML-generated suggestions for the user: relevant jobs, programs, etc.
class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=True)  # Optional: may be null

    # A numerical score from ML, indicating how relevant this recommendation is
    score = db.Column(db.Float)

    # Type of recommendation: job, training, or protection (used for filtering)
    type = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Represents insight or updates shared by users about their local community or situation.
class NoticeBoard(db.Model):
    __tablename__ = 'notice_boards'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # What the user wrote
    location = db.Column(db.String(100))  # Optional: could be different from user.location

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Represents an internal admin who manages users and stakeholder accounts.
class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)