"""Flagged concept Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation_flask import app
from graph_curation.apis.flag_dependent_concept import \
            flagged_dependent_concept_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2


POST_REQUEST = "POST"
FLAGED_CONCEPT_API = "/flagged-concept"


class Flaggedconcept(_Resource):
    """Handeler for Adding flagged concept to database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add flagged concept to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.FlagDependentConcept, FLAGED_CONCEPT_API,
            POST_REQUEST)

        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], FLAGED_CONCEPT_API,
                POST_REQUEST
            )
        try:
            app.logger.error("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Entered Flagged API%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            flagged_concept_response =\
                flagged_dependent_concept_query_response(
                    request.concept_key, request.nested_concept_key,
                    request.flagged_by
                )
            response = _api_output_pb2.Acknowledgement()
            flagged_concept_result = _json_format.ParseDict(
                flagged_concept_response, response)
            return flask_request_response.message_response(
                flagged_concept_result,
                FLAGED_CONCEPT_API, POST_REQUEST, 200)
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], FLAGED_CONCEPT_API, POST_REQUEST
            )
