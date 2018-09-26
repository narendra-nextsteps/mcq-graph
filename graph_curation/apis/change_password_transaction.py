"""Change password query."""
# from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def change_password_query(currentPassword, newPassword, userKey):
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
    function() {
        let currentPassword = "%s",
        newPassword = "%s",
        userKey = "%s"
        let db = require('@arangodb').db
        let userCheck = db._query(`
            LET doc = DOCUMENT(CONCAT('Users/', @userKey))
            RETURN IS_NULL(doc) ? {
                "is_successful_execution": false,
                "execution_error_messages": [
                    "username: @userKey doesn't exist."
                ]
            } : (
                @currentPassword == doc.password ? {
                    "is_successful_execution": true
                } : {
                    "is_successful_execution": false,
                    "execution_error_messages": [
                        "username: @userKey current password doesn't match."
                    ]
                }
            )
        `, {userKey: userKey, currentPassword: currentPassword}).toArray()[0]
        if (!userCheck.is_successful_execution) return userCheck

        if (currentPassword === newPassword) return {
            "is_successful_execution": false,
            "execution_error_messages":["both new and old are same passwords."]
        }

        db._query(`
            LET doc = DOCUMENT(CONCAT('Users/', @userKey))
            UPDATE doc WITH {
                password: @newPassword
            }
            In Users
            RETURN true
        `, {newPassword: newPassword, userKey: userKey}).toArray()[0]

        return {"is_successful_execution": true}
        }
    """ % (currentPassword, newPassword, userKey)


def change_password_query_response(currentPassword, newPassword, userKey):
    """Show the successful or error message for the changed password.

    Parameters
    ----------
    currentPassword : string
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
    query_response = _db_objects.graph_db().transaction({
        "write": ["Users"],
        "read": ["Users"]
        }, change_password_query(currentPassword, newPassword, userKey))
    print(query_response)
    if query_response['error']:
        return {"is_successful_execution": False}
    return query_response['result']
