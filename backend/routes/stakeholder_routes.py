from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from models.models import db, User, UserProfile

stakeholder_bp = Blueprint('stakeholder', __name__)

@stakeholder_bp.route('/get_organization_data')
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