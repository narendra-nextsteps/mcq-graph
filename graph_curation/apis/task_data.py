"""Query to get all tasks."""
from graph_curation.db import db_nomenclature, db_objects


def task_data_query(username):
    """Query to get all tasks."""
    return """
        LET chapters = (
            FOR chapter IN {chapters}
                FILTER chapter.locked_to == "{username}"
                RETURN chapter
        )

        RETURN {{
            chapters: chapters,
            is_successful_execution: True
        }}
    """.format(chapters=db_nomenclature.CHAPTER_COLLECTION, username=username)


def task_data_query_response(username):
    """Response to api call for tasks assigned to a user.

    Parameters
    ----------
    uid : strig

    Returns
    -------
    array
        response form the db query for asigned tasks.

    """
    query_response = \
        db_objects.graph_db().AQLQuery(
            task_data_query(username)
        ).response

    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    data = query_response["result"][0]
    return data
