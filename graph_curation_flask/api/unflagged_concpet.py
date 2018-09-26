"""Unflagged concept Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.unflag_dependent_concept import \
            unflagged_dependent_concept_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2


POST_REQUEST = "POST"
UNFLAGED_CONCEPT_API = "/unflagged-concept"


class Unflaggedconcept(_Resource):
    """Handeler for adding unflagged concept to database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Added unflagged concept to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.UnFlagDependentConcept, UNFLAGED_CONCEPT_API,
            POST_REQUEST)
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], UNFLAGED_CONCEPT_API,
                POST_REQUEST
            )
        try:
            unflaged_concept_response = \
                                    unflagged_dependent_concept_query_response(
                                        request.concept_key,
                                        request.nested_concept_key,
                                        request.unflagged_by
                                    )
            response = _api_output_pb2.Acknowledgement()
            result = _json_format.ParseDict(
                unflaged_concept_response, response
            )
            return flask_request_response.message_response(
                result,
                UNFLAGED_CONCEPT_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], UNFLAGED_CONCEPT_API, POST_REQUEST
            )
