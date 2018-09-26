"""Get all assigned task Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_all_assign_tasks import \
    get_all_assign_task_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
ALL_ASSIGNED_TASK_API = "/get-all-assigned-task"


class AllAssignmetsDataRest(_Resource):
    """Handeler for Getting All assigned task data Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Get all the assigned task data."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.GetSubTasks, ALL_ASSIGNED_TASK_API, POST_REQUEST)

        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], ALL_ASSIGNED_TASK_API,
                POST_REQUEST
            )
        try:
            all_assigned_task_response = get_all_assign_task_query_response(
                request.username
            )
            response = _api_output_pb2.GetAllAssignedTasks()
            ass_assign_task_result = _json_format.ParseDict(
                all_assigned_task_response, response
            )
            return flask_request_response.message_response(
                ass_assign_task_result,
                ALL_ASSIGNED_TASK_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], ALL_ASSIGNED_TASK_API, POST_REQUEST
            )
