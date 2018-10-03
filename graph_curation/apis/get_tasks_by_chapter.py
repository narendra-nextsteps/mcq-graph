"""Get assignment data from the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_tasks_by_chapter_query(chapter_key):
    """Query users, chapters, tasks in the db.

    Returns
    -------
    dict
        return all users, chapters, tasks.

    """
    return """
        LET tasks = (
            FOR task IN {tasks_collection}
                FILTER task.chapter_key == "{chapter_key}"
                RETURN {{
                    "task_key": task._key,
                    "status": task.status,
                    "assigned_to": task.assigned_to,
                    "chapter_key": task.chapter_key,
                    "chapter": task.chapter,
                    "assigned_time": task.assigned_time
                }}
        )
        RETURN {{
            tasks: tasks
        }}
    """.format(
        tasks_collection=_db_nomenclature.TASK_COLLECTION,
        chapter_key=chapter_key
    )


def get_tasks_by_chapter_response(chapter_key):
    """Query all assignment in the db.

    Returns
    -------
    api_output_pb2.GetAllUsers
        return all users username,first name,last name,email.

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_tasks_by_chapter_query(chapter_key)
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
