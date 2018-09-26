"""Superadmin dashboard Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_superadmin_dashboard import \
        get_superadmin_dashboard_query_response
from graph_curation.protos import api_output_pb2 as _api_output_pb2

GET_REQUEST = "GET"
SUPER_ADMIN_DASHBOARD_API = "/get-super-admin-dashboard"


class SuperAdminDashboardDataRest(_Resource):
    """Handeler for getting superAdmin dashboard data Rest api."""
    @jwt_required
    def get(self):
        """Get all the tasks for super admin dashboard."""
        try:
            users_task_data = get_superadmin_dashboard_query_response()
            response = _api_output_pb2.GetSuperAdminDashboard()
            result = _json_format.ParseDict(users_task_data, response)
            return flask_request_response.message_response(
                result,
                SUPER_ADMIN_DASHBOARD_API, GET_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], SUPER_ADMIN_DASHBOARD_API, GET_REQUEST
            )
