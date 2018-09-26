"""Rest apis."""

from flask_restful import Resource as _Resource, Api as _Api

from graph_curation_flask import app, \
    flask_request_response
from graph_curation import sample

API = _Api(app)

POST_REQUEST = "POST"
GET_REQUEST = "GET"

SAMPLE_API = "/sample"


class SampleRest(_Resource):
    """Sample Rest api."""

    def get(self):
        """Says hi to cookiecutter."""
        return flask_request_response.json_response(
            {"text": sample()},
            SAMPLE_API, GET_REQUEST, 200
        )

    def post(self):
        """Says hi to given name."""
        request, err = flask_request_response.json_request(
            SAMPLE_API, POST_REQUEST
        )
        if err is not None:
            return flask_request_response.json_response(
                {"error_message": str(err)}, SAMPLE_API, POST_REQUEST, 400
            )
        if "name" not in request:
            return flask_request_response.json_response(
                {"error_message": "Unable to find the 'name' in the request"},
                SAMPLE_API, POST_REQUEST, 400
            )
        return flask_request_response.json_response(
            {"text": sample(request["name"])},
            SAMPLE_API, POST_REQUEST, 200
        )


API.add_resource(SampleRest, SAMPLE_API)
