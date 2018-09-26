"""Assigned task Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation_flask import app
from graph_curation.apis.assign_task import assign_task_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2


POST_REQUEST = "POST"
ASSIGN_TASK_API = "/assign-task"


class AssignTask(_Resource):
    """Handeler for Adding assigned task to resultbase Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add assigned task of the user into database."""
        app.logger.error("####################assign_task_query_response Done####################")
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.AssignTask, ASSIGN_TASK_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message["err_message"]], ASSIGN_TASK_API, POST_REQUEST
            )
        try:
            app.logger.error("In API calling assign_task_query_response")
            assign_task_response = assign_task_query_response(
                request.assigned_by, request.assigned_to_list,
                request.chapter_key
            )
            app.logger.error("####################assign_task_query_response Done####################")
            app.logger.info(assign_task_response)
            return flask_request_response.json_response(
                assign_task_response,
                ASSIGN_TASK_API, POST_REQUEST, 200
            )
        except Exception as err:
            app.logger.error("*********************" + str(err) + "**********************************")
            return flask_request_response.error_response(
                [str(err)], ASSIGN_TASK_API, POST_REQUEST
            )
