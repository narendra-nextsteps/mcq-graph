"""Change password Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.change_password_transaction import change_password_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
CHANGE_PASSWORD_API = "/change-password"


class ChangePasswordData(_Resource):
    """Handeler for Updating new password to database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Update new password to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.ChangePassword, CHANGE_PASSWORD_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], CHANGE_PASSWORD_API,
                POST_REQUEST
            )
        try:
            change_password_response = change_password_query_response(
                request.current_password, request.new_password,
                request.user_key
            )
            response = _api_output_pb2.Acknowledgement()
            change_password_result = _json_format.ParseDict(
                change_password_response, response
            )
            return flask_request_response.message_response(
                change_password_result,
                CHANGE_PASSWORD_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], CHANGE_PASSWORD_API, POST_REQUEST
            )
