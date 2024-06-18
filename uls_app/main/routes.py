from datetime import datetime, timedelta
from functools import wraps
from jwt import decode, encode, DecodeError, ExpiredSignatureError
from flask import jsonify, make_response, request
from uls_app.main import bp
from uls_app.models.user import User
from config import Localconfig

#Define you token here
def token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token=None
        
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        response = {"message": {"error": ""}}

        if not token:
            response["message"]["error"] = "token missing"
            return make_response(response, 401)
        
        jwt_data=None
        try:
            jwt_data = decode(
                token,
                Localconfig.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
            user = User.query.filter_by(name=jwt_data["name"]).first()
            if not user:
                response["message"][
                    "error"
                ] = f"User {jwt_data['name']} doesn't exist"
                return make_response(response, 404)

            token_exp = datetime.utcfromtimestamp(jwt_data["exp"])
            current_time = datetime.utcnow()
            if token_exp < current_time:
                response["message"]["error"] = "Token expired"
                return make_response(response, 401)
            
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        
        return f(*args, **kwargs)
    
    return decorator

@bp.route("/login", methods=["POST"])
def login():
    name = request.json.get("name","")
    password = request.json.get("password","")
    
    user = User.query.filter_by(name=name).first()

    if not user:
        return (
            jsonify({"message": {"error": "User {} doesn't exist".format(name)}}),
            400,
        )
    if not user.check_password(password):
        return (
            jsonify({"message": {"error": "Wrong credentials."} }), 400
        )
    
    jwt = encode(
        {
            "name" : name,
            "user_id" : user.id,
            "exp" : datetime.utcnow() + timedelta(minutes=2),
        },
        Localconfig.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    
    return (
        jsonify(
            {   
                "status": "ok",
                "jwt" : jwt,
                "name": name,
                "user_id": user.id,
                "exp": (datetime.utcnow() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
            }
        ),
        200,
    )