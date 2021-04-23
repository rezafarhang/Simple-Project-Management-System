from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login_preview():
    return json.dumps(
        {
            'data': 'you can sign in with your info'
        }
    )


@auth.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    user_email = json_data.get('email')
    user_password = json_data.get('password')

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return json.dumps(
            {
                'status_code': '404',
                'message': 'User Not Found'
            }
        )

    elif not check_password_hash(user.password, user_password):
        return json.dumps(
            {
                'status_code': '403',
                'message': 'Wrong Password'
            }
        )

    login_user(user)
    print(user.is_authenticated)
    return json.dumps(
        {
            'status_code': '200',
            'message': 'Login Sucessfully'
        }
    )


@auth.route('/signups', methods=['GET'])
def signup_preview():
    return json.dumps({'data': 'submit your info for sigunp'})


@auth.route('/signups', methods=['POST'])
def signup_post():
    json_data = request.get_json()
    user_id = json_data.get('id')
    user_name = json_data.get('fullname')
    user_email = json_data.get('email')
    user_password = json_data.get('password')

    user = User.query.filter_by(email=user_email).first()

    if user:
        return json.dumps(
            {
                'status_code': '409',
                'message': 'This Email Already Exist'
            }
        )
    elif not user_name or not user_password:
        return json.dumps(
            {
                'status_code': '404',
                'message': 'Enter Your Info'
            }
        )

    db.session.add(
        User(
            id=user_id,
            fullname=user_name,
            email=user_email,
            password=generate_password_hash(user_password, method='sha256')
        )
    )
    db.session.commit()

    return json.dumps(
        {
            'status_code': '201',
            'message': 'User Created Sucessfully'
        }
    )


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return json.dumps(
        {
            'status_code': '200',
            'message': 'Logout Sucessfully'
        }
    )
