"""Curation concept complete Api."""
from flask_restful import Resource as _Resource
from google.protobuf import json_format as _json_format
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.delete_dependent_concept import \
        delete_dependent_concept_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2
from graph_curation.protos import api_output_pb2 as _api_output_pb2

POST_REQUEST = "POST"
DELEETE_CONCEPT_API = "/delete-concept"


class DeleteConceptData(_Resource):
    """Handeler for adding Delete concept from the database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add delete concept value and add user to database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.DeleteDependentConcept, DELEETE_CONCEPT_API,
            POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], DELEETE_CONCEPT_API,
                POST_REQUEST
            )
        try:
            delete_concept_response = delete_dependent_concept_query_response(
                request.concept_key, request.nested_concept_key,
                request.deleted_by
            )
            response = _api_output_pb2.Acknowledgement()
            delete_concept_result = _json_format.ParseDict(
                delete_concept_response, response)
            return flask_request_response.message_response(
                delete_concept_result,
                DELEETE_CONCEPT_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], DELEETE_CONCEPT_API, POST_REQUEST
            )
