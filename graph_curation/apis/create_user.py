"""Create new user query."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects
from graph_curation.protos import database_pb2 as _database_pb2


def create_user_query(username, password, first_name, last_name, email, role):
    """Create user query.

    Parameters
    ----------
    username : string
        unique username
    password : string
        password can't be empty
    first_name : string
        first name of the user
    last_name : string
        last name of the user
    role : string
        role can be SME,SUPER_ADMIN,ADMIN
    """
    return """
        INSERT {{
            "username": "{username}",
            "password": "{password}",
            "first_name": "{first_name}",
            "last_name": "{last_name}",
            "role": "{role}",
            "email":"{email}",
            "_key": "{username}"
        }}
        IN {user_collection}
        RETURN {{
            is_successful_execution: true
        }}
    """.format(
        username=username, password=password,
        first_name=first_name, last_name=last_name, email=email, role=role,
        user_collection=_db_nomenclature.USER_COLLECTION
    )


def user_exist_or_not(username):
    """Check wheter the username exist or not.

    Parameters
    ----------
    username : string
        unique username in the collection users

    Returns
    -------
            return true if user exist else insert new user.

    """
    return """
        LET username = "{username}"
        RETURN IS_NULL(DOCUMENT(CONCAT("{user_collection}/",username)))
    """.format(
        username=username,
        user_collection=_db_nomenclature.USER_COLLECTION
    )


def create_user_query_response(
        username, password, first_name, last_name, email, role):
    """Create user query response.

    Parameters
    ----------
    username : string
        unique username
    password : string
        password can't be empty
    first_name : string
        first name of the user
    last_name : string
        last name of the user
    role : database_pb2.UserDocument.UserRole.Enum
        role is UsersDocument.UserRole.Enum

    Returns
    -------
    api_output_pb2.Acknowledgement
        return sucessful execution true when user name is unique.

    """
    is_user_exist_query_response = \
        _db_objects.graph_db().AQLQuery(user_exist_or_not(username)).response
    if is_user_exist_query_response['result'][0] is True:
        query_response = \
            _db_objects.graph_db().AQLQuery(
                create_user_query(
                    username, password, first_name, last_name, email,
                    _database_pb2.UsersDocument.UserRole.Enum.Name(role)
                )
            ).response
        if query_response['error'] or len(query_response['result']) is 0:
            return {"is_successful_execution": False, "msg": "err"}
        return query_response['result'][0]
    return {
        "is_successful_execution": False,
        "execution_error_messages": ["User exist's"]
    }
