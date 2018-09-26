"""delete user query."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def delete_user_query(username):
    """delete user query.

    Parameters
    ----------
    username : string
        unique username

    """
    return """
LET username = "{username}"

FOR u IN {user_collection}
filter u.username==username
  REMOVE{{ "_key": u.username}}
IN {user_collection}

RETURN {{
    is_successful_execution: true
}}
    """.format(
        username=username,
        user_collection=_db_nomenclature.USER_COLLECTION
        )


def delete_user_query_response(username):
    """delete user query response.

    Parameters
    ----------
    username : string
        unique username

    Returns
    -------
    api_output_pb2.Acknowledgement
        return sucessful execution true when user name is unique.

    """

    query_response = \
        _db_objects.graph_db().AQLQuery(
            delete_user_query(
                username
            )
        ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
