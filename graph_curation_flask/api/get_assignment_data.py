"""Get Assignments data Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_assignment_data \
    import get_assignment_data_response
from graph_curation.protos import api_output_pb2 as _api_output_pb2

GET_REQUEST = "GET"
ASSIGNMENT_DATA_API = "/get-assignment-data"


class GetAssignmentsData(_Resource):
    """Handeler for Geting all users data Rest api."""

    @jwt_required
    def get(self):
        """Get data for assignment."""
        try:
            assignment_data = get_assignment_data_response()
            response = _api_output_pb2.GetAssignmentData()
            assignment_result = \
                _json_format.ParseDict(assignment_data, response)
            return flask_request_response.message_response(
                assignment_result,
                ASSIGNMENT_DATA_API, GET_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], ASSIGNMENT_DATA_API, GET_REQUEST
            )
