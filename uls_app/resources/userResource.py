from flask import abort
from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy.exc import IntegrityError
from uls_app.extensions import db
from uls_app.main.routes import token_required
from uls_app.models.user import User

parser = reqparse.RequestParser()
parser.add_argument("name",type=str,required=True)
parser.add_argument("password",type=str,required=True)
parser.add_argument("userType",type=str,required=True)

user_fields={
    "id": fields.Integer,
    "name": fields.String,
    "password": fields.String,
    "userType": fields.String,
}

def if_user_not_exists(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404, {"error": "User {} doesn't exist".format(user_id)})

class UserResource(Resource):
    @token_required
    @marshal_with(user_fields)
    def get(self, user_id=None):
        if user_id:
            if_user_not_exists(user_id)
            user = User.query.filter_by(id=user_id).first()
            print("Fetching user from database")
            return user, 200
        else:
            users=User.query.all()
            print("Fetching all users from databse")
            return users, 200

    @marshal_with(user_fields)
    def put(self, user_id=None):
        if not user_id:
            abort(404, {"error": "Invalid user_id {}.".format(user_id)})
        else:    
            if_user_not_exists(user_id)
            args = parser.parse_args()
            user = User.query.filter_by(id=user_id).first()
            for arg in args:
                if args[arg] is not None:
                    setattr(user, arg, args[arg])
            db.session.commit()
            return user, 200

    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        user = User(**args)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(409, "User already exists")
        return user, 201

    @marshal_with(user_fields)
    def delete(self, user_id):
        if not user_id:
            abort(404, {"error": "Invalid user_id {}.".format(user_id)})
        else:
            if_user_not_exists(user_id)
            user = User.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
            return user, 200