"""Logout User Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from graph_curation_flask import flask_request_response
from graph_curation.db.collection_insertion import insert_revoked_token


POST_REQUEST = "POST"
LOGOUT_API = "/logout"


class LogOutRest(_Resource):
    """Handeler for getting logout user Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Logout response."""
        try:
            jti = get_raw_jwt()['jti']
            revoked_token = insert_revoked_token(jti)
            print(revoked_token)
            return flask_request_response.json_response(
                {'is_successful_execution': True}, LOGOUT_API,
                POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], LOGOUT_API, POST_REQUEST
            )
