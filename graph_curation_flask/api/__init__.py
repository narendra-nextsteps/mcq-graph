"""All Rest apis for graph curation."""
from flask_restful import Api as _Api
from graph_curation_flask import app
from graph_curation.apis.jti_blacklisted import is_jti_blacklisted

from . import \
    get_user_dashboard, get_super_admin_dashboard, \
    curation_concpet_completed, create_user, change_password, \
    get_all_users, assign_task, \
    login, logout, get_refresh_token, delete_user, \
    abort_task, get_assignment_data, task_data, sub_task_data, \
    get_dependent_concepts, add_edge, delete_edge, get_tasks_by_chapter

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
    task_data.TaskData,
    task_data.TASK_DATA_API
)

API.add_resource(
    get_tasks_by_chapter.GetTasksByChapter,
    get_tasks_by_chapter.GET_TASKS_BY_CHAPTER_API
)

API.add_resource(
    sub_task_data.SubTaskData,
    sub_task_data.SUB_TASK_DATA_API
)

API.add_resource(
    get_dependent_concepts.GetDependentConcepts,
    get_dependent_concepts.DEPENDENT_CONCEPTS_API
)

API.add_resource(
    get_assignment_data.GetAssignmentsData,
    get_assignment_data.ASSIGNMENT_DATA_API
)

API.add_resource(
    add_edge.AddEdge,
    add_edge.ADD_EDGE_API
)

API.add_resource(
    delete_edge.DeleteEdge,
    delete_edge.DELETE_EDGE_API
)

API.add_resource(
    get_refresh_token.RefreshRest, get_refresh_token.REFRESH_TOKEN_API
)

API.add_resource(
    assign_task.AssignTask, assign_task.ASSIGN_TASK_API
)
API.add_resource(
    abort_task.AbortTAsk, abort_task.ABORT_TASK_API
)

API.add_resource(
    get_all_users.AllUsersDataRest,
    get_all_users.USERS_DATA_API
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
    logout.LogOutRest,
    logout.LOGOUT_API
)
API.add_resource(
    login.LoginRest,
    login.LOGIN_API
)
