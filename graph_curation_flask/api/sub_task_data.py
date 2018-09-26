"""Get all assigned tasks."""

from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.protos import api_input_pb2 as _api_input_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2
from graph_curation.apis.sub_task_data import sub_task_data_query_response

POST_REQUEST = "POST"
SUB_TASK_DATA_API = "/sub-task-data"


class SubTaskData(_Resource):
    """Handler to get all sub tasks assigned to user."""

    from flask import request

    def post(self):
        """Request for sub tasks."""

        request, error_message = flask_request_response.message_request(
            _api_input_pb2.SubTaskData, SUB_TASK_DATA_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message'], "msg response"],
                SUB_TASK_DATA_API,
                POST_REQUEST
            )
        try:
            print("==========>")

            sub_task_data_response = sub_task_data_query_response(
                request.chapter_id
            )
            response = _api_output_pb2.SubTaskData()
            sub_task_data_result = _json_format.ParseDict(
                sub_task_data_response, response
            )
            return flask_request_response.message_response(
                sub_task_data_result,
                SUB_TASK_DATA_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err), "try response"], SUB_TASK_DATA_API, POST_REQUEST
            )
