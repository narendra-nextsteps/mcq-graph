"""Get selected concept data from db api."""
from flask_restful import Resource as _Resource
from graph_curation_flask import flask_request_response
from flask_jwt_extended import jwt_required
from graph_curation.apis.get_selected_concept import \
        get_selected_concept_query_response
from graph_curation.protos import api_input_pb2 as _api_intput_pb2

POST_REQUEST = "POST"
SELECTED_CONCEPT_API = "/get-selected-concept"


class SelectedConceptDataRest(_Resource):
    """Handeler for getting Selected concept data Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Get selected concept data from the  database."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.GetSelectedConcept, SELECTED_CONCEPT_API,
            POST_REQUEST
        )

        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], SELECTED_CONCEPT_API,
                POST_REQUEST
            )
        try:
            concept_response = get_selected_concept_query_response(
                request.concept_key
            )
            return flask_request_response.json_response(
                concept_response,
                SELECTED_CONCEPT_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], SELECTED_CONCEPT_API, POST_REQUEST
            )
