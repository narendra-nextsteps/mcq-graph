"""Utils for requests in flask."""

import json as _json
from flask import request as _request, make_response as _make_response
from graph_curation_flask import app
from google.protobuf import json_format as _json_format


def json_request(api_name, request_type, encoding='utf-8'):
    """Json Request.

    Parameters:
    ----------
    api_name : string
        Name of the api.
    request_type : string
        POST or GET.

    """
    try:
        request_text = _request.data
        json_object = _json.loads(request_text.decode(encoding))
        app.logger.info(
            "Request for '%s/%s': %s",
            api_name, request_type, _json.dumps(json_object, indent=2)
        )
    except Exception:
        app.logger.error(
            "Unable to parse the given text: %s in %s/%s",
            request_text, api_name, request_type
        )
        return None
    return json_object


def json_response(json_object, api_name, request_type, status_code=200):
    """Create a rest response of content-type application/json.

    Parameters:
    ----------
    json_object : dict|list
        Response json object.
    api_name: string
        Name of the api.
    request_type: string
        Type of the request.
    status_code : int
        (the default is 200)

    Returns
    -------
    flask.Response

    """
    json_string = _json.dumps(json_object, indent=2)
    app.logger.info(
        "Response from '%s/%s': %s",
        api_name, request_type, json_string
    )
    response = _make_response(json_string)
    response.headers['content-type'] = "application/json"
    response.status_code = status_code
    return response


def text_response(response_text, api_name, request_type, status_code=200):
    """Create a rest response of content-type text/plain.

    Parameters:
    ----------
    response_text : string
        Response text.
    api_name: string
        Name of the api.
    request_type: string
        Type of the request.
    status_code : integer, optional
        (the default is 200)

    Returns
    -------
    flask.Response

    """
    app.logger.info(
        "Response from '%s/%s': '%s'",
        api_name, request_type, response_text
    )
    response = _make_response(response_text)
    response.headers['content-type'] = "text/plain"
    response.status_code = status_code
    return response


def message_request(message_creator, api_name, request_type, encoding='utf-8'):
    """Convert the json request into message.

    If there is an error in parsing the message then return the according error
    else return message.

    Parameters:
    ----------
    message_creator : ProtoMessage
        Message Creater class.
    api_name: string
        Name of the api.
    request_type: string
        Type of the request.

    Returns
    -------
    Message, Error
        Parse to the given Message creator.

    """
    json_message = json_request(api_name, request_type, encoding)
    if json_message is None:
        return None, {"err_message": "Unable to parse json"}
    try:
        message = message_creator()
        _json_format.ParseDict(json_message, message)
        app.logger.info(
            "message Request for '%s/%s'\n%s",
            api_name, request_type, message
        )
    except _json_format.ParseError:
        return None, {"err_message": "Unable to parse json to proto"}
    except Exception as err:
        return None, {"err_message": str(err)}
    return message, None


def message_response(
        message, api_name, request_type, status_code=200,
        preserving_proto_field_name=True,
        including_default_value_fields=False
):
    """Create a rest response of content-type application/json for message.

    Parameters:
    ----------
    message : Protobuf Message
        Protobuf message to be sent as json.
    api_name : string
        Name of the api.
    request_type : string
        Type of the request.
    status_code : integer, optional
        (the default is 200)
    preserving_proto_field_name : bool, optional
        (the default is True)
    including_default_value_fields : bool, optional
        (the default is False)

    Returns
    -------
    flask.Response

    """
    return json_response(
        _json_format.MessageToDict(
            message, preserving_proto_field_name=preserving_proto_field_name,
            including_default_value_fields=including_default_value_fields
        ), api_name, request_type, status_code
    )


def error_response(error_messages, api_name, request_type):
    """Create a error response of content-type application/json for errors.

    Parameters:
    ----------
    error_message : string
        error in the execution
    api_name : string
        Name of the api.
    request_type : string
        Type of the request.

    Returns
    -------
    flask.Response

    """
    return json_response({
        "is_successful_execution": False,
        "error_messages": error_messages
    }, api_name, request_type, 400)