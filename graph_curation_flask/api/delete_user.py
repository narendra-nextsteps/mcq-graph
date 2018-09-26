"""delete user Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.delete_user import delete_user_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2


POST_REQUEST = "POST"
DELETE_USER_API = "/delete-user"


class DeleteUserData(_Resource):
    """Handeler for deleting user from database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Delete user from database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.DeleteUser, DELETE_USER_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.message_response(
                [error_message['err_message']], DELETE_USER_API, POST_REQUEST
            )
        try:
            delete_user_response = delete_user_query_response(
                request.username
            )
            return flask_request_response.json_response(
                delete_user_response,
                DELETE_USER_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], DELETE_USER_API, POST_REQUEST
            )
