"""Get user dashboard."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_user_dashboard_query(username):
    """Get the USer dashboard for the userid.

    Parameters
    ----------
    username : string
        username for searching all task for that user

    Returns
    -------
    string
        get user dashboard query

    """
    return """
LET username = "{username}"

LET tasks = (
    FOR task_doc in {task_collection}
        FILTER task_doc.assigned_to == username
        LET sub_tasks = (
            FOR sub_task_doc in {sub_task_collection}
            FILTER sub_task_doc.task_key == task_doc._key
            RETURN {{
                    sub_task_key: sub_task_doc._key,
                    sub_task_status: sub_task_doc.status,
                    concept_key: sub_task_doc.concept_key,
                    concept: sub_task_doc.concept_name
            }}
        )
        RETURN {{
            sub_tasks: sub_tasks,
            chapter: task_doc.chapter,
            chapter_key: task_doc.chapter_key,
            task_key: task_doc.task_key,
            task_status: task_doc.status
        }}
)

RETURN {{
    tasks: tasks,
    is_successful_execution: true
}}
    """.format(
        username=username,
        task_collection=_db_nomenclature.TASK_COLLECTION,
        sub_task_collection=_db_nomenclature.SUBTASK_COLLECTION
    )


def get_user_dashboard_query_response(username):
    """Get the user dashboard query response.

    Parameters
    ----------
    username : string
        username for searching all task for that user
    Returns
    api_output_pb2.GetUserDashboard
                Return all the sub task assigned to the user.

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_user_dashboard_query(username)).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
