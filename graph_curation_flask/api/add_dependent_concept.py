"""Add Dependent concept to db Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.add_dependent_concept import \
                add_dependent_concept_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2


POST_REQUEST = "POST"
ADD_DEPENDENT_CONCEPT_API = "/add-dependent-concept"


class AddDependentData(_Resource):
    """Handeler for Adding dependent concpet data to db Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add dependent concept to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.AddDependentConcept, ADD_DEPENDENT_CONCEPT_API,
            POST_REQUEST
        )

        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']],
                ADD_DEPENDENT_CONCEPT_API, POST_REQUEST
            )

        try:
            dependent_concept_response = add_dependent_concept_query_response(
                request.concept_key, request.dependent_concept_name,
                request.dependent_concept_key, request.created_by
            )
            response = _api_output_pb2.AddDependentConcept()
            dependent_concept_result = _json_format.ParseDict(
                dependent_concept_response, response
            )
            return flask_request_response.message_response(
                dependent_concept_result, ADD_DEPENDENT_CONCEPT_API,
                POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], ADD_DEPENDENT_CONCEPT_API, POST_REQUEST
            )
