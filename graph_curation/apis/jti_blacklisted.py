"""Checkiing the token is blacklisted or not."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def is_jti_blacklisted_query(jti):
    """Query for checking the jti id is exist or not in db


    Parameters
    ----------
    jti : string
        jti id to check in the db
    Returns
    -------
    string
        query for checking token is blacklisted or not

    """
    return """
RETURN {{
    "is_blacklisted": DOCUMENT("{revoked_collection}/{jti}") != NULL
}}
    """.format(
        jti=jti, revoked_collection=_db_nomenclature.REVOKED_TOKEN_COLLECTION
    )


def is_jti_blacklisted(jti):
    """Query response for checking the jti id is exist or not in db.

    Parameters
    ----------
    jti : string
        jti id to check in the db

    Returns
    dict
        access token is blacklisted or not

    """
    query_response = _db_objects.graph_db().AQLQuery(
        is_jti_blacklisted_query(jti)).response
    print(query_response)
    if query_response['error'] or len(query_response['result']) is 0:
        return None
    return query_response['result'][0]['is_blacklisted']
