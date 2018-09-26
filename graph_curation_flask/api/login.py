"""Login User Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from graph_curation_flask import flask_request_response
from graph_curation.apis.login import login_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2

POST_REQUEST = "POST"
LOGIN_API = "/login"


class LoginRest(_Resource):
    """Handeler for getting login user Rest api."""

    from flask import request

    def post(self):
        """Login verification."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.Login, LOGIN_API, POST_REQUEST
        )
        print(error_message)
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], LOGIN_API,
                POST_REQUEST
            )
        try:
            access_token = create_access_token(identity=request.username)
            refresh_token = create_refresh_token(identity=request.username)
            login_response = login_query_response(
                request.username, request.password
            )
            print(login_response)
            login_response['access_token'] = access_token
            login_response['refresh_token'] = refresh_token
            return flask_request_response.json_response(
                login_response,
                LOGIN_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], LOGIN_API, POST_REQUEST
            )
