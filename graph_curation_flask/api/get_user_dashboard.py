"""User dashboard Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_user_dashboard import \
        get_user_dashboard_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
USER_DASHBOARD_API = "/get-user-dashboard"


class UserDashboardDataRest(_Resource):
    """Handeler for getting user dashboard data Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Get all the task assigned for the user dashboard."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.GetUserDashboard, USER_DASHBOARD_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], USER_DASHBOARD_API,
                POST_REQUEST
            )
        try:
            user_dashboard_response = get_user_dashboard_query_response(
                request.username)
            response = _api_output_pb2.GetUserDashboard()
            result = _json_format.ParseDict(user_dashboard_response, response)
            return flask_request_response.message_response(
                result,
                USER_DASHBOARD_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], USER_DASHBOARD_API, POST_REQUEST
            )
