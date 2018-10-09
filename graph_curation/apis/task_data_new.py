"""Query to get all tasks."""
from graph_curation.db import db_nomenclature, db_objects
from graph_curation.utils import text_content_tree


def task_data_query(username):
    """Query to get all tasks."""
    return """

        FOR text IN TextSelectionContent
            RETURN text
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
    # print(query_response['result'][0])
    print("=======================")
    print(query_response['error'])
    if query_response['error'] or len(query_response['result']) is 0:
        return {
            "is_successful_execution": False, 
            "err": query_response['error']
        }
    data = text_content_tree.get_text_contents(query_response["result"])
    print(data)
    return data
