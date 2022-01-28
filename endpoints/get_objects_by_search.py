from flask import jsonify
import flask
from db import db

from models.app_users import AppUser, user_schema
from lib.authenticate import authenticate_return_auth
from util.validate_uuid4 import validate_uuid4
import endpoints

@authenticate_return_auth
def get_objects_by_search(req:flask.Request, search_term, auth_info) -> flask.Response:
    user_data = db.session.query(AppUser).filter(AppUser.user_id == auth_info.user.user_id).first()
   
    
    search_results = {}
    search_results["users"] = endpoints.users_get_by_search(req, search_term, True, auth_info)
    return jsonify(search_results)