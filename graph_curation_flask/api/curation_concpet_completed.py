"""Curation concept complete Api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.completed_task import \
            complete_task_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2


POST_REQUEST = "POST"
CURATION_CONCEPT_COMPLETE_API = "/curation-concept-complete"


class CurationConceptCompleteData(_Resource):
    """Handeler for adding complete concept curation to database Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Add complete status to the curated concept in database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.CurationConceptCompleted,
            CURATION_CONCEPT_COMPLETE_API, POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], CURATION_CONCEPT_COMPLETE_API,
                POST_REQUEST
            )
        try:
            concept_response = complete_task_query_response(
                    request.chapter_key, request.mcq_key
            )
            return flask_request_response.json_response(
                concept_response,
                CURATION_CONCEPT_COMPLETE_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], CURATION_CONCEPT_COMPLETE_API, POST_REQUEST
            )
