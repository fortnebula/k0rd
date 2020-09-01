from flask import Flask
from flask_restx import Api
import api.auth.routes as auth
import api.cluster.routes as cluster


def register_routes(app: Flask) -> None: # noqa
    api = Api(app) # noqa
    api.add_resource(auth.Version, '/v1')
    api.add_resource(auth.UserList, '/v1/user/list')
    api.add_resource(auth.UserCreate, '/v1/user/create')
    api.add_resource(auth.IssueTokens, '/v1/token/issue')
    api.add_resource(auth.RefreshTokens, '/v1/token/refresh')
    api.add_resource(auth.IssueApiTokens, '/v1/token/api/issue')
    api.add_resource(auth.RevokeApiTokens, '/v1/token/api/revoke')
    api.add_resource(cluster.ClusterList, '/v1/cluster/list')
    api.add_resource(cluster.ClusterCreate, '/v1/cluster/create')
    api.add_resource(cluster.ClusterUpdateStatus, '/v1/cluster/update/status')
    api.add_resource(cluster.ClusterUpdateIp, '/v1/cluster/update/ip')
    api.add_resource(cluster.ClusterUpdateVersion,
                     '/v1/cluster/update/version')
