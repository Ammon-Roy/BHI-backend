from flask import jsonify
import flask
from db import db
from models.app_users import AppUser, users_schema
from lib.authenticate import authenticate_return_auth
from datetime import datetime
from util.validate_uuid4 import validate_uuid4
from util.foundation_utils import strip_phone


@authenticate_return_auth
def user_add(req:flask.Request, bcrypt, auth_info) -> flask.Response:
    post_data = req.get_json()
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    password = post_data.get('password')
    phone = post_data.get('phone')
    active = post_data.get('active')
    created_date = datetime.now()
    role = post_data.get('role')
    print(role)
    if (role == None or role in ['super-admin', 'admin', 'user']):
        role = 'user'
        
        if auth_info.user.role != 'super-admin':
            if role == 'super-admin':
                role = 'user'
        
        if active == None:
            active = True

        hashed_password = bcrypt.generate_password_hash(password).decode("utf8")
        stripped_phone = strip_phone(phone)
        record = AppUser(first_name, last_name, email, hashed_password, stripped_phone, created_date, role, active)

        db.session.add(record)
        db.session.commit()

        return jsonify("User created"), 201
    else:
        return jsonify("ERROR: user role not in list"), 400