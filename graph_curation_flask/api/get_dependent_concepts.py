"""Get all assigned tasks."""

from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from graph_curation_flask import flask_request_response
from graph_curation.protos import api_input_pb2 as _api_input_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2
from graph_curation.apis.get_dependent_concepts  \
    import dependent_concepts_query_response

POST_REQUEST = "POST"
DEPENDENT_CONCEPTS_API = "/get-dependent-concepts"


class GetDependentConcepts(_Resource):
    """Handler to get dependents for a contcept."""

    from flask import request

    def post(self):
        """Request for dependent concepts."""

        request, error_message = flask_request_response.message_request(
            _api_input_pb2.GetDependentConcepts, DEPENDENT_CONCEPTS_API,
            POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message'], "msg response"],
                DEPENDENT_CONCEPTS_API,
                POST_REQUEST
            )
        try:
            dependent_concepts_response = dependent_concepts_query_response(
                request.concept_id, request.mcq_id
            )
            response = _api_output_pb2.GetDependentConcepts()
            dependent_concepts_result = _json_format.ParseDict(
                dependent_concepts_response, response
            )
            return flask_request_response.message_response(
                dependent_concepts_result,
                DEPENDENT_CONCEPTS_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err), "try response"], DEPENDENT_CONCEPTS_API,
                POST_REQUEST
            )
