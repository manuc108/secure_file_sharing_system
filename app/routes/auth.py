from flask import Blueprint, request, jsonify
from app.services.auth import signup_user, verify_email, login_user

bp = Blueprint('auth', __name__)

@bp.route('/')
def home():
    return jsonify(message="Welcome to the Secure File Sharing System!")
    

@bp.route('/signup', methods=['POST'])
def signup():
    # Handle user signup
    data = request.get_json() 
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(message="Email and password are required."), 400
    result, status_code = signup_user(data['email'], data['password'])
    return jsonify(result), status_code
    

@bp.route('/verify-email/<token>', methods=['GET'])
def verify(token):
    # Verify user email with the token
    if not token:
        return jsonify(message="Verification token is required."), 400
    result, status_code = verify_email(token)
    return jsonify(result), status_code
    

@bp.route('/login', methods=['POST'])
def login():
    # Handle user login
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(message="Email and password are required."), 400
    result, status_code = login_user(data['email'], data['password'])
    return jsonify(result), status_code
