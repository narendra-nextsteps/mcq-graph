"""Get all assigned tasks."""
import json
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.protos import api_input_pb2 as _api_input_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2
from graph_curation.apis.add_edge  \
    import add_edge_query_response

POST_REQUEST = "POST"
ADD_EDGE_API = "/add-edge"


class AddEdge(_Resource):
    """Handler to add a dependent contcept."""

    from flask import request

    def post(self):
        """Add dependent concepts."""
        msg_request, error_message = \
            flask_request_response.message_request(
                _api_input_pb2.AddEdge, ADD_EDGE_API,
                POST_REQUEST
            )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message'], "msg response"],
                ADD_EDGE_API,
                POST_REQUEST
            )
        try:
            json_message = \
                flask_request_response.json_request(ADD_EDGE_API, POST_REQUEST)
            print(json.dumps(json_message, indent=2))
            add_dependent_concepts_response = add_edge_query_response(
                json_message["edges"]
            )
            response = _api_output_pb2.AddEdge()
            print("==========>", response, type(response))
            add_dependent_concepts_result = _json_format.ParseDict(
                add_dependent_concepts_response, response
            )
            return flask_request_response.message_response(
                add_dependent_concepts_result,
                ADD_EDGE_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err), "try response"], ADD_EDGE_API,
                POST_REQUEST
            )
