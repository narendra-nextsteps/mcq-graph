"""Selection data api."""
from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from graph_curation_flask import flask_request_response
from graph_curation.apis.get_seletion_data import \
    get_selection_data_result
from graph_curation.protos import api_input_pb2 as _api_intput_pb2

POST_REQUEST = "POST"
SELECTION_DATA_API = "/selection-data"


class SelectionDataRest(_Resource):
    """Handeler for getting SelectionData user Rest api."""

    from flask import request

    @jwt_required
    def post(self):
        """Selection data of chapters according to proto response."""
        request, error_message = flask_request_response.message_request(
            _api_intput_pb2.GetSelectionData, SELECTION_DATA_API,
            POST_REQUEST
        )
        if error_message is not None:
            return flask_request_response.error_response(
                [error_message['err_message']], SELECTION_DATA_API,
                POST_REQUEST
            )
        try:
            selection_data_response = get_selection_data_result(
                request.username
            )
            return flask_request_response.json_response(
                selection_data_response,
                SELECTION_DATA_API, POST_REQUEST, 200
            )
        except Exception as err:
            return flask_request_response.error_response(
                [str(err)], SELECTION_DATA_API, POST_REQUEST
            )
