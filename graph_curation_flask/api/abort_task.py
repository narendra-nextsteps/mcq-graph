"""Abort task Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.abort_task import \
            abort_task_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2


POST_REQUEST = "POST"
ABORT_TASK_API = "/abort-task"


class AbortTAsk(_Resource):
    """Handeler for aborting a task Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Abort a task."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.AbortTask, ABORT_TASK_API,
            POST_REQUEST)

        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], ABORT_TASK_API,
                POST_REQUEST
            )
        try:
            flagged_concept_response =\
                abort_task_query_response(
                    request.chapter_key, request.username
                )
            response = _api_output_pb2.Acknowledgement()
            flagged_concept_result = _json_format.ParseDict(
                flagged_concept_response, response)
            return flask_request_response.message_response(
                flagged_concept_result,
                ABORT_TASK_API, POST_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], ABORT_TASK_API, POST_REQUEST
            )
