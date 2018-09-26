"""Get superadmin dashboard."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_superadmin_dashboard_query():
    """Get all the Assigned task to the all the users.

    Returns
    -------
    string
        get superadmin dashboard query

    """
    return """
        LET tasks = (
        FOR task_doc in {task_collection}
        RETURN {{
                chapter_key: task_doc.chapter_key,
                chapter: task_doc.chapter,
                assigned_to: task_doc.assigned_to,
                completed_time: task_doc.completed_time,
                status:task_doc.status
            }}
        )
        RETURN {{
            tasks: tasks,
            is_successful_execution: true
        }}
    """.format(
        task_collection=_db_nomenclature.TASK_COLLECTION
    )


def get_superadmin_dashboard_query_response():
    """Get the superadmin dashboard query response.

    Returns
    -------
    api_output_pb2.GetSuperAdminDashboard
        superadmin dashboard

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_superadmin_dashboard_query()).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
