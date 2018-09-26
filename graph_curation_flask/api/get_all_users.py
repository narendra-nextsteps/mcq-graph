"""Get all users data Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_all_users import get_all_users_query_response
from graph_curation.protos import api_output_pb2 as _api_output_pb2

GET_REQUEST = "GET"
USERS_DATA_API = "/get-all-users"


class AllUsersDataRest(_Resource):
    """Handeler for Geting all users data Rest api."""

    @jwt_required
    def get(self):
        """Get all the users data."""
        try:
            users_data = get_all_users_query_response()
            response = _api_output_pb2.GetAllUsers()
            users_result = _json_format.ParseDict(users_data, response)
            return flask_request_response.message_response(
                users_result,
                USERS_DATA_API, GET_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], USERS_DATA_API, GET_REQUEST
            )
