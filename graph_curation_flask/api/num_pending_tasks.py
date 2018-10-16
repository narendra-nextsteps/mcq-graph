"""Get all assigned tasks."""

from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.protos import api_input_pb2 as _api_input_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2
from graph_curation.apis.num_pending_tasks import num_pending_tasks_response

POST_REQUEST = "POST"
PENDING_TASKS_API = "/num-pending-tasks"


class PendingTasks(_Resource):
    """Handler to get all tasks assigned to user."""

    from flask import request

    def post(self):
        """Request for tasks."""

        request, error_message = flask_request_response.message_request(
            _api_input_pb2.NumPendingTasks, PENDING_TASKS_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message'], "msg response"],
                PENDING_TASKS_API, POST_REQUEST
            )
        try:
            task_data_response = num_pending_tasks_response(request.username)
            response = _api_output_pb2.NumPendingTasks()
            task_data_result = _json_format.ParseDict(
                task_data_response, response
            )
            return flask_request_response.message_response(
                task_data_result,
                PENDING_TASKS_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err), "try response"], PENDING_TASKS_API, POST_REQUEST
            )
