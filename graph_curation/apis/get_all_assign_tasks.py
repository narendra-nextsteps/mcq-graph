"""Get all the assignmant for that user."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_all_assign_task_query(username):
    """Get all the Assigned task to the all the users.

    Parameters
    ----------
    username : string
        superadmin

    Returns
    string
        query for getting all assigned task

    """
    return """
LET username = "{username}"
LET assignments = (
    FOR task_doc in {task_collection}
        FILTER task_doc.assigned_by == "{username}"
        RETURN KEEP(task_doc, [
            "chapter_key", "chapter", "assigned_to",
            "assigned_time", "completed_time", "status"
        ])
)
RETURN {{
    assignments: assignments,
    is_successful_execution: true
}}
        """.format(
            username=username,
            task_collection=_db_nomenclature.TASK_COLLECTION
            )


def get_all_assign_task_query_response(username):
    """Get all the Assigned task query response.

    Parameters
    ----------
    username : string
        superadmin

    Returns
    api_output_pb2.GetAllAssignedTasks
        return chapter_key,chapter,assigned_to,assigned_time,completed_time,
        status

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_all_assign_task_query(username)).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
