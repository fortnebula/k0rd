"""This module provides routes as classes so they can be called
in the main application"""
from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity,
                                jwt_required, get_raw_jwt, get_jti,
                                jwt_optional)

# Local module imports
from api.database import db_session as db
from api.models import users
from api.config import config

ADMIN_TOKEN = config.ADMIN_TOKEN


class Version(Resource):
    """default function is to provide the api version and possibily
    list available endpoints"""
    def get(self):
        """Responds back with the api version"""
        response = jsonify({"version": "v0.0.1"})
        return (response.json), 200


class IssueTokens(Resource):
    """This endpoint grabs a token authentication is successful"""
    def get(self):
        """get request should return what this endpoint can do"""
        response = jsonify({"msg": "Post username and password"})
        return (response.json), 200

    def post(self):
        """A post request to this endpoint takes the username and
        password submitted via json and checks the database to ensure
        a match before issuing a token"""
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            response = jsonify({"msg": "Missing username parameter"})
            return (response.json), 400
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            return (response.json), 400
        query = users.User.query.filter_by(username=username).first()
        if query.verify_password(password) is True:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = jsonify(access_token=access_token,
                               refresh_token=refresh_token)
            return (response.json), 200
        response = jsonify({"msg": "unauthenticated"})
        return (response.json), 401


class RefreshTokens(Resource):
    """This endpoint grabs a token authentication is successful"""
    def get(self):
        """get request should return what this endpoint can do"""
        response = jsonify({"msg": "Post username and password"})
        return (response.json), 200

    @jwt_refresh_token_required
    def post(self):
        """A post request to this endpoint takes the username and
        password submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        create_new_token = create_access_token(identity=current_user)
        response = jsonify(access_token=create_new_token)
        return (response.json), 200


class UserCreate(Resource):
    """This endpoint registers users to the system. Currently any users
    may be registered, nothing is checked to make sure a user is authorized
    to do so"""
    def get(self):
        """get request should return what this endpoint can do"""
        response = jsonify({"msg": "Post username and password"})
        return (response.json), 200

    @jwt_optional
    def post(self):
        """A post request to this method will take the username and
        password from json and add them to the database. Passwords are
        salted before being placed into the database"""
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        role = request.json.get('role', 'member')
        admin_token = request.headers.get('x-admin-token')
        if not username:
            response = jsonify({"msg": "Missing username parameter"})
            return (response.json), 400
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            return (response.json), 400
        if admin_token:
            if admin_token != ADMIN_TOKEN:
                response = jsonify({"msg": "invalid admin token"})
                return (response.json), 401
            elif admin_token == ADMIN_TOKEN:
                db.add(users.User(username, password, role))
                db.commit()
                response = jsonify(status='registered', username=username)
                return (response.json), 200
        current_user = get_jwt_identity()
        query = users.User.query.filter_by(username=current_user).first()
        if query.role == 'admin':
            db.add(users.User(username, password, role))
            db.commit()
            response = jsonify(status='registered', username=username)
            return (response.json), 200
        response = jsonify({"msg": "admin user account required"})
        return (response.json), 400


class UserList(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def get(self):
        """get request should return what this endpoint can do"""
        query = users.User.query.all()
        response = jsonify(query)
        return (response.json), 200


class IssueApiTokens(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        api_key = create_access_token(identity=current_user,
                                      expires_delta=False)
        api_key_jti = get_jti(encoded_token=api_key)
        revoked = False
        query = users.User.query.filter_by(username=current_user).first()
        db.add(users.Tokens(query.uuid, revoked, api_key_jti))
        db.commit()
        response = jsonify(api_key=api_key)
        return (response.json), 200


class RevokeApiTokens(Resource):

    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def delete(self):
        blacklist = set()
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        users.Tokens.query.filter_by(api_key=jti).update(dict(revoked=True))
        db.commit()
        response = jsonify({"msg": "Successfully deleted token"})
        return (response.json), 200
