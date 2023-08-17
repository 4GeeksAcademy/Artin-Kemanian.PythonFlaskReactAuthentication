"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    print(user)

    if user == None:
        return jsonify({"msg": "This email doesn't exist"}), 401

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# @api.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     user = User.query.filter_by(email=current_user).first()
#     response_body = {
#         "msg": "Usuario encontrado",
#         "usuario": user.serialize(),
#     }

#     return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    print(body)

    user = User.query.filter_by(email=body["email"]).first()
    print(user)
    if user == None:
        user = User(email=body["email"], password=body["password"], is_active=True)
        db.session.add(user)
        db.session.commit()
        response_body = {
            "msg": "Usuario creado"
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Usuario ya creado con ese correo"}), 401

if __name__ == "__main__":
    api.run()