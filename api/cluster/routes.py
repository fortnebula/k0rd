from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database import db_session as db
from api.models import users, clusters


class ClusterList(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def get(self):
        """get request should return what this endpoint can do"""
        current_user = get_jwt_identity()
        query = users.User.query.filter_by(username=current_user).first()
        response = jsonify(query.clusters)
        return (response.json), 200


class ClusterCreate(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def post(self):
        """A post request to this endpoint takes the base_image and
        user_image submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        if current_user is None:
            response = jsonify({"msg": "unauthenticated"})
            return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        mac_address = request.json.get('mac', None)
        ip_address = request.json.get('ip', None)
        status = request.json.get('status', None)
        version = request.json.get('version', None)
        if not mac_address:
            response = jsonify({"msg": "Missing mac parameter"})
            return (response.json), 400
        query = users.User.query.filter_by(username=current_user).first()
        cluster = clusters.Cluster(query.uuid, mac_address, ip_address,
                                   status, version)
        db.add(cluster)
        db.commit()
        response = jsonify(status=status, id=cluster.uuid)
        return (response.json), 200


class ClusterUpdateStatus(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def put(self):
        """A post request to this endpoint takes the base_image and
        user_image submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        if current_user is None:
            response = jsonify({"msg": "unauthenticated"})
            return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        mac_address = request.json.get('mac', None)
        status = request.json.get('status', None)
        if not mac_address or not status:
            response = jsonify({"msg": "Missing parameter"})
            return (response.json), 400
        clusters.Cluster.query.filter_by(mac_address=mac_address
                                         ).update(dict(status=status))
        db.commit()
        response = jsonify(status=status, mac=mac_address)
        return (response.json), 200


class ClusterUpdateIp(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def put(self):
        """A post request to this endpoint takes the base_image and
        user_image submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        if current_user is None:
            response = jsonify({"msg": "unauthenticated"})
            return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        mac_address = request.json.get('mac', None)
        ip_address = request.json.get('ip', None)
        if not mac_address or not ip_address:
            response = jsonify({"msg": "Missing parameter"})
            return (response.json), 400
        clusters.Cluster.query.filter_by(mac_address=mac_address
                                         ).update(dict(ip_address=ip_address))
        db.commit()
        response = jsonify(ip_address=ip_address, mac=mac_address)
        return (response.json), 200


class ClusterUpdateVersion(Resource):
    """This endpoint grabs a token authentication is successful"""
    @jwt_required
    def put(self):
        """A post request to this endpoint takes the base_image and
        user_image submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        if current_user is None:
            response = jsonify({"msg": "unauthenticated"})
            return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        mac_address = request.json.get('mac', None)
        version = request.json.get('version', None)
        if not mac_address or not version:
            response = jsonify({"msg": "Missing parameter"})
            return (response.json), 400
        clusters.Cluster.query.filter_by(mac_address=mac_address
                                         ).update(dict(version=version))
        db.commit()
        response = jsonify(version=version, mac=mac_address)
        return (response.json), 200
