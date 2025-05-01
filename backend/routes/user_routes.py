from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models.models import db, UserProfile

user_bp = Blueprint('user', __name__)

@user_bp.route('/add_user_profile', methods=['POST'])
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