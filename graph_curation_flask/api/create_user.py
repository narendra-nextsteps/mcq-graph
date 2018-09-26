"""Create user Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.create_user import create_user_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2


POST_REQUEST = "POST"
CREATE_USER_API = "/create-user"


class CreateUserData(_Resource):
    """Handeler for adding new user to database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add new user to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.CreateUser, CREATE_USER_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.message_response(
                [error_message['err_message']], CREATE_USER_API, POST_REQUEST
            )
        try:
            create_user_response = create_user_query_response(
                request.username, request.password, request.first_name,
                request.last_name, request.email, request.role
            )
            response = _api_output_pb2.CreateUser()
            create_user_result = _json_format.ParseDict(
                create_user_response, response
            )
            return flask_request_response.message_response(
                create_user_result,
                CREATE_USER_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], CREATE_USER_API, POST_REQUEST
            )
