"""Get all the users into the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_all_users_query():
    """Query all users in the db.

    Returns
    -------
    dict
        return all users username,first name,last name,email.

    """
    return """
        LET users = (
        FOR users in {user_collection}
        RETURN {{
            username: users.username,
            first_name: users.first_name,
            last_name: users.last_name,
            email: users.email,
            role:users.role
        }}
        )
        RETURN {{
            users: users,
            is_successful_execution: true
        }}
    """.format(user_collection=_db_nomenclature.USER_COLLECTION)


def get_all_users_query_response():
    """Query all users in the db.

    Returns
    -------
    api_output_pb2.GetAllUsers
        return all users username,first name,last name,email.

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_all_users_query()
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
