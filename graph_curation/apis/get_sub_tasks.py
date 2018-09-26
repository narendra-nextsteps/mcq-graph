"""Get all the subtask."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_sub_tasks_query(username):
    """Get all the subtask for the userid.

    Parameters
    ----------
    username : string
        username for searching all task for that user

    Returns
    -------
    string
        Return query for getting all the sub task assigned to the user.

    """
    return """
LET username = "{username}"

LET subtasks = (
    FOR task_doc in {task_collection}
        FILTER task_doc.assigned_to == "{username}"
        FOR sub_task_doc in {sub_task_collection}
            FILTER sub_task_doc.task_key == task_doc._key
            RETURN {{
                "sub_task_key": sub_task_doc._key,
                "sub_task_status": sub_task_doc.status,
                "concept_key": sub_task_doc.concept_key,
                "concept": sub_task_doc.concept
            }}
)
RETURN {{
    sub_tasks: subtasks,
    is_successful_execution: true
}}
        """.format(
            username=username,
            task_collection=_db_nomenclature.TASK_COLLECTION,
            sub_task_collection=_db_nomenclature.SUBTASK_COLLECTION
        )


def get_sub_tasks_query_response(username):
    """Get all the sub task query response.

    Parameters
    ----------
    username : string
        username for searching all task for that user

    Returns
    -------
    api_output_pb2.GetSubTasks
        return subtask for the user

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_sub_tasks_query(username)).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
