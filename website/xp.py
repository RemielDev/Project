from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from .models import User
from . import db

xp = Blueprint('xp', __name__)




@xp.route('/update_xp', methods=['POST'])
@login_required
def update_xp():
    """Endpoint to update user XP and level."""
    data = request.get_json()
    xp_gained = data.get('xp', 0)
    xp_per_level = 100

    current_user.xp += xp_gained

    # Handle level-up
    if current_user.xp >= xp_per_level:
        current_user.xp -= xp_per_level
        current_user.level += 1

    db.session.commit()

    return jsonify({'level': current_user.level, 'xp': current_user.xp})

@xp.route('/get_user_data', methods=['GET'])
@login_required
def get_user_data():
    """Endpoint to fetch user XP and level."""
    return jsonify({'xp': current_user.xp, 'level': current_user.level})