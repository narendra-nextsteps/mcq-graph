"""User login and authentication."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def login_query(username, password):
    """Search the username and password matched or not.

    Parameters
    ----------
    username : string
        username who is getting login
    password : string
        password of that username

    Returns
    -------
    string
        query for login

    """
    return """
        LET username = "{username}"
        LET password =  "{password}"
        LET user_doc = DOCUMENT(CONCAT("{user_collection}/", username))

        FILTER user_doc.username == username
        FILTER user_doc.password == password
            RETURN {{
                user_key: user_doc._key,
                user_role: user_doc.role,
                is_successful_execution: true
            }}
    """.format(
        username=username, password=password,
        user_collection=_db_nomenclature.USER_COLLECTION
    )


def login_query_response(username, password):
    """Get the login credientails message success or failed.

    Parameters
    ----------
    username : string
        username who is getting login
    password : string
        password of that username

    Returns
    -------
    api_output_pb2.Login
        return successful execution true and access token and refresh token

    """
    query_response = _db_objects.graph_db().AQLQuery(
        login_query(username, password)).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
