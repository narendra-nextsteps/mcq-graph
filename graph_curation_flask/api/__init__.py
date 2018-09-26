"""All Rest apis for graph curation."""
from flask_restful import Api as _Api
from graph_curation_flask import app
from graph_curation.apis.jti_blacklisted import is_jti_blacklisted

from . import \
    add_flagged_concept, get_user_dashboard, get_super_admin_dashboard, \
    curation_concpet_completed, create_user, change_password, \
    get_selected_concept, get_all_users, \
    unflagged_concpet, get_all_assigned_tasks, get_sub_task, \
    add_dependent_concept, assign_task, deleted_concept, \
    get_selection_data, login, logout, get_refresh_token, delete_user, \
    abort_task, get_assignment_data

from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
API = _Api(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Checking the token is blacklisted or not.

    Parameters
    ----------
    decrypted_token : string
        token for checking

    Returns
    -------
    boolean
        true or false by checking token
    """

    jti = decrypted_token['jti']
    return is_jti_blacklisted(jti)


API.add_resource(
    get_assignment_data.GetAssignmentsData,
    get_assignment_data.ASSIGNMENT_DATA_API
)

API.add_resource(
    get_refresh_token.RefreshRest, get_refresh_token.REFRESH_TOKEN_API
)

API.add_resource(
    add_flagged_concept.Flaggedconcept, add_flagged_concept.FLAGED_CONCEPT_API
)

API.add_resource(
    unflagged_concpet.Unflaggedconcept, unflagged_concpet.UNFLAGED_CONCEPT_API
)

API.add_resource(
    add_dependent_concept.AddDependentData,
    add_dependent_concept.ADD_DEPENDENT_CONCEPT_API
)
API.add_resource(
    assign_task.AssignTask, assign_task.ASSIGN_TASK_API
)
API.add_resource(
    abort_task.AbortTAsk, abort_task.ABORT_TASK_API
)
API.add_resource(
    deleted_concept.DeleteConceptData, deleted_concept.DELEETE_CONCEPT_API
)
API.add_resource(
    get_sub_task.AllSubTasksDataRest, get_sub_task.SUB_TASK_API
)
API.add_resource(
    get_all_assigned_tasks.AllAssignmetsDataRest,
    get_all_assigned_tasks.ALL_ASSIGNED_TASK_API
)
API.add_resource(
    get_all_users.AllUsersDataRest,
    get_all_users.USERS_DATA_API
)
API.add_resource(
    get_selected_concept.SelectedConceptDataRest,
    get_selected_concept.SELECTED_CONCEPT_API
)
API.add_resource(
    change_password.ChangePasswordData,
    change_password.CHANGE_PASSWORD_API
)
API.add_resource(
    create_user.CreateUserData,
    create_user.CREATE_USER_API
)
API.add_resource(
    delete_user.DeleteUserData,
    delete_user.DELETE_USER_API
)
API.add_resource(
    curation_concpet_completed.CurationConceptCompleteData,
    curation_concpet_completed.CURATION_CONCEPT_COMPLETE_API
)
API.add_resource(
    get_super_admin_dashboard.SuperAdminDashboardDataRest,
    get_super_admin_dashboard.SUPER_ADMIN_DASHBOARD_API
)
API.add_resource(
    get_user_dashboard.UserDashboardDataRest,
    get_user_dashboard.USER_DASHBOARD_API
)
API.add_resource(
    get_selection_data.SelectionDataRest,
    get_selection_data.SELECTION_DATA_API
)
API.add_resource(
    logout.LogOutRest,
    logout.LOGOUT_API
)
API.add_resource(
    login.LoginRest,
    login.LOGIN_API
)
