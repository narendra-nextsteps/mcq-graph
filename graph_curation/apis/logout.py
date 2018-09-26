"""Logout query."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def logout_query(username):
    """Logout from the session.

    Parameters
    ----------
    username : string
        username who is getting logout

    Returns
    -------
    string
        query for logout

    """
    return """
LET username = "{username}"
LET user_doc = DOCUMENT(CONCAT("{user_collection}/", username))

FILTER user_doc.username == username

RETURN {{
    is_successful_execution: true
}}
        """.format(
            username=username,
            user_collection=_db_nomenclature.USER_COLLECTION
            )


def logout_query_response(username):
    """Get the logout message success or failed.

    Parameters
    ----------
    username : string

    Returns
    dict
        return successful execution true or false

    """
    query_response = _db_objects.graph_db().AQLQuery(
        logout_query(username)).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
