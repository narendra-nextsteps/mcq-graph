function changePassword() {
    let currentPassword = 'current_password',
        newPassword = 'new_password',
        userKey = '324'
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
        "execution_error_messages": ["both new and old are same passwords."]
    }

    db._query(`
        LET doc = DOCUMENT(CONCAT('Users/', @userKey))
        UPDATE doc WITH {
            password: @newPassword
        }
        In Users
        RETURN true
    `, {newPassword: newPassword, userKey: userKey})

    return {"is_successful_execution": true}
}