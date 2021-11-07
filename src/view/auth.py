#  Copyright (c) Fahad Ahammed 2021.
import redis
from flask import jsonify, request
from flask_jwt_extended import get_jwt, jwt_required, create_access_token

from src import ACCESS_EXPIRES, app, jwt
from src.model.user import User

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(
    host=app.config.get("REDIS_HOST"), port=app.config.get("REDIS_PORT"), db=app.config.get("REDIS_DB"),
    decode_responses=True
)


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@app.route(f"/api/{app.config.get('API_VERSION')}/registration", methods=["POST"])
def registration():
    return User().create_user(userObject=request.json)


@app.route(f"/api/{app.config.get('API_VERSION')}/login", methods=["POST"])
def login():
    user_ok = User().check_user_auth(email=request.json.get("email"), password=request.json.get("password"))
    if user_ok:
        user_info = User().get_user(email=request.json.get("email"))
        user_info.pop("password")
        access_token = create_access_token(identity=user_info)
        access_token_with_bearer = f"Bearer {access_token}"
        return jsonify(msg="Successfully logged in !", access_token=access_token, access_token_with_bearer=access_token_with_bearer,
                       user_info=user_info, status="success")
    else:
        return jsonify(msg="Wrong email or password !", status="error")


# Endpoint for revoking the current users access token. Save the JWTs unique
# identifier (jti) in redis. Also set a Time to Live (TTL)  when storing the JWT
# so that it will automatically be cleared out of redis after the token expires.
@app.route(f"/api/{app.config.get('API_VERSION')}/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")