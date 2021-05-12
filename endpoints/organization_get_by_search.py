from flask import jsonify
import flask
from db import db
from models.organizations import Organization, organizations_schema
from lib.authenticate import authenticate_return_auth
from util.validate_uuid4 import validate_uuid4

@authenticate_return_auth
def organization_get_by_search(req:flask.Request, search_term, internal_call, p_auth_info, auth_info) -> flask.Response:
    auth_info = {}
    if internal_call == False:
        auth_info = validate_auth_token(request.headers.get("auth_token"))
    elif p_auth_info:
        auth_info = p_auth_info
    
    if not auth_info:
        return jsonify("Access Denied"), 401
    
    search_term = search_term.lower()
    
    org_query = db.session.query(Organization)\
        .filter(db.or_( \
            db.func.lower(Organization.name).contains(search_term), \
            Organization.phone.contains(search_term), \
            db.func.lower(Organization.city).contains(search_term), \
            db.func.lower(Organization.state).contains(search_term)\
        ))

    if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
        org_query.filter(Organization.org_id == auth_info.user.org_id)\
    
    org_data = org_query.order_by(Organization.name.asc()).all()
    if (internal_call):
        return organizations_schema.dump(org_data)
    
    return jsonify(organizations_schema.dump(org_data))