"""Get all assigned tasks."""

from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.protos import api_input_pb2 as _api_input_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2
from graph_curation.apis.delete_edge  \
    import delete_edge_query_response

POST_REQUEST = "POST"
DELETE_EDGE_API = "/delete-edge"


class DeleteEdge(_Resource):
    """Handler to add a dependent contcept."""

    from flask import request

    def post(self):
        """Add dependent concepts."""
        request, error_message = flask_request_response.message_request(
            _api_input_pb2.DeleteEdge, DELETE_EDGE_API,
            POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message'], "msg response"],
                DELETE_EDGE_API,
                POST_REQUEST
            )
        try:
            delete_edge_response = delete_edge_query_response(
                request.edge_id,
                request.username
            )
            response = _api_output_pb2.DeleteEge()
            print("==========>", response, type(response))
            delete_edge_result = _json_format.ParseDict(
                delete_edge_response, response
            )
            return flask_request_response.message_response(
                delete_edge_result,
                DELETE_EDGE_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err), "try response"], DELETE_EDGE_API,
                POST_REQUEST
            )
