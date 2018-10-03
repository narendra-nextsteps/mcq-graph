"""Get Assignments data Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
# from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_tasks_by_chapter \
    import get_tasks_by_chapter_response
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
GET_TASKS_BY_CHAPTER_API = "/get-tasks-by-chapter"


class GetTasksByChapter(_Resource):
    """Handeler for Geting all users data Rest api."""

    from flask import request

    def post(self):
        """Get data for assignment."""
        try:
            json_message = \
                flask_request_response.json_request(
                    GET_TASKS_BY_CHAPTER_API,
                    POST_REQUEST
                )
            assignment_data = \
                get_tasks_by_chapter_response(json_message["chapter_key"])
            response = _api_output_pb2.GetTasksByChapter()
            assignment_result = \
                _json_format.ParseDict(assignment_data, response)
            return flask_request_response.message_response(
                assignment_result,
                GET_TASKS_BY_CHAPTER_API, POST_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], GET_TASKS_BY_CHAPTER_API, POST_REQUEST
            )
