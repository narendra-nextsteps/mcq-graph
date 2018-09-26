"""Get sub task Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_sub_tasks import get_sub_tasks_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
SUB_TASK_API = "/get-sub-tasks"


class AllSubTasksDataRest(_Resource):
    """Handeler for getting sub task data for the user Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Get all sub task data for user from database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.GetSubTasks, SUB_TASK_API, POST_REQUEST)
        print(request)
        print(error_message)
        if error_message is not None:
            return flask_request_response.message_response(
                [error_message['err_message']], SUB_TASK_API, POST_REQUEST
            )
        try:
            message_response = get_sub_tasks_query_response(
                request.username
                    )
            print(message_response)
            response = _api_output_pb2.GetSubTasks()
            result = _json_format.ParseDict(message_response, response)
            return flask_request_response.message_response(
                result,
                SUB_TASK_API, POST_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], SUB_TASK_API, POST_REQUEST
            )
