from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db import db
import marshmallow as ma


class AppUser(db.Model):
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    phone = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(), default='user', nullable=False)
    auth = db.relationship('AuthToken', backref = 'user')

    def __init__(self, first_name, last_name, email, password, phone, created_date, role, active = True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.created_date = created_date
        self.role = role
        self.active = active
   
   
class AppUserSchema(ma.Schema):
    class Meta:
        fields = ['user_id','first_name', 'last_name', 'email', 'password', 'phone', 'created_date', 'role', 'active']

    
user_schema = AppUserSchema()
users_schema = AppUserSchema(many=True)