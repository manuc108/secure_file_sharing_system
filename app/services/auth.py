import datetime
import jwt
from flask import current_app
from app import mongo
from app.models import User
from bson.objectid import ObjectId
from smtp2go.core import Smtp2goClient


EMAIL_PAYLOAD = """
Hello,
This email address was used to create an account in Secure File Sharing System:

------------------------------------------
email: {email}
time: {time} UTC
------------------------------------------

Click the link below to verify your email address. This link will expire in 24 hours:
{verification_url}

If this isn't you, please ignore this email.
"""

def signup_user(email, password):
    # Register a new user and send a verification email.
    if mongo.db.users.find_one({'email': email}):
        return {'message': 'User already exists!'}, 400

    new_user = User(email=email, password=password)
    result = new_user.save()

    verification_token = generate_verification_token(str(result.inserted_id))

    if not current_app.config['TESTING']:
        verification_url = f"{current_app.config['BASE_URL']}/verify-email/{verification_token}"
        send_verification_email(email, verification_url)

    return {
        'message': 'User created successfully. Check your email for the verification link, which expires in 24 hours.'
    }, 201


def generate_verification_token(user_id):
    # Generate a JWT token for email verification.
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    return jwt.encode({
        'user_id': user_id,
        'exp': expiration
    }, current_app.config['SECRET_KEY'], algorithm="HS256")


def send_verification_email(email, verification_url):
    # Send a verification email with the verification link.
    smtp_client = Smtp2goClient(current_app.config['SMTP2GO_API_KEY'])
    email_content = EMAIL_PAYLOAD.format(
        email=email,
        time=str(datetime.datetime.utcnow())[:19],
        verification_url=verification_url
    )
    smtp_client.send(
        sender=current_app.config['SMTP2GO_SENDER'],
        recipients=[email],
        subject='Email Verification - Secure File Sharing System',
        text=email_content
    )


def verify_email(token):
    # Verify email using the provided token.
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})

        if not user:
            return {'message': 'User not found'}, 404

        mongo.db.users.update_one({'_id': ObjectId(data['user_id'])}, {'$set': {'verified': True}})
        return {'message': 'Email verified successfully'}, 200

    except jwt.ExpiredSignatureError:
        return {'message': 'Verification link has expired'}, 400
    except jwt.InvalidTokenError:
        return {'message': 'Invalid verification link'}, 400


def login_user(email, password):
    # Authenticate user and generate JWT token.
    user = mongo.db.users.find_one({'email': email})

    if not user or not User.check_password(user['password'], password):
        return {'message': 'Invalid credentials'}, 401

    if user['role'] == 'client' and not user.get('verified', False):
        return {'message': 'Please verify your email first'}, 401

    token = generate_verification_token(str(user['_id']))
    return {'token': token}, 200
