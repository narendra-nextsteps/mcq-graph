"""Refresh token Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import create_access_token, get_jwt_identity,\
    jwt_refresh_token_required
from graph_curation_flask import flask_request_response


POST_REQUEST = "GET"
REFRESH_TOKEN_API = "/refresh-token"


class RefreshRest(_Resource):
    """Handeler for getting Refresh Token Rest api."""

    @jwt_refresh_token_required
    def get(self):
        """Refresh Token."""
        current_user = get_jwt_identity()
        print(current_user)
        refresh_token = {
            'access_token': create_access_token(identity=current_user)
        }
        return flask_request_response.json_response(
            refresh_token, REFRESH_TOKEN_API, POST_REQUEST, 200
        )
