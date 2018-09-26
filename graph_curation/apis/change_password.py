"""Change password query."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def change_password_query(current_password, new_password, user_key):
    """Show the successful or error message for the changed password.

    Parameters
    ----------
    current_password : string
        current password of the user
    new_password : string
        new password for the user
    user_key : string
        for which username password is getting updated

    Returns
    -------
    string
        query to update the password

    """
    return """
LET doc_key = "{user_key}"
LET doc = DOCUMENT(CONCAT("{user_collection}/", doc_key))

LET current_password = "{current_password}"
LET new_password = "{new_password}"

FILTER doc.password == current_password AND doc.password != new_password

    UPDATE doc WITH {{
        "password": new_password
    }}

IN {user_collection}
RETURN {{
    is_successful_execution: true
}}
    """.format(
        current_password=current_password, new_password=new_password,
        user_key=user_key,
        user_collection=_db_nomenclature.USER_COLLECTION
    )


def change_password_query_response(current_password, new_password, user_key):
    """Show the successful or error message for the changed password.

    Parameters
    ----------
    current_password : string
        user's current password
    new_password : string
        user's new password that is getting updated
    user_key :string
        for which username password is getting update
    Returns
    -------
    api_output_pb2.Acknowledgemet
        return valid execution true or flase

    """
    query_response = \
        _db_objects.graph_db().AQLQuery(
            change_password_query(current_password, new_password, user_key)
        ).response
    print(query_response)
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
