"""Query to get text and concepts of the particular context."""

import json
from graph_curation.db import db_nomenclature, db_objects


def sub_task_data_query(chapter_id):
    """Query to get sub tasks from the db.

    Parameters
    ----------
    chapter_id : string
        id of the paricular context to curate.

    """
    return """
        LET chapter_id = "{chapter_id}"
        LET mcqs = (
            FOR mcq IN {McqsTable}
                FILTER mcq.chapterId == chapter_id
                RETURN mcq
        )
        RETURN {{
            mcqs: mcqs,
            is_successful_execution: True
        }}
        """.format(
            chapter_id=chapter_id,
            McqsTable=db_nomenclature.VIDEOS_COLLECTION
        )


def sub_task_data_query_response(chapter_id):
    """Response to api call for subtasks.

    [description]
    Using "text id" a db query is run to get sub tasks on that id.
    """
    query_response = db_objects.graph_db().AQLQuery(
        sub_task_data_query(chapter_id)
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    print(json.dumps(query_response["result"], indent=2))

    return query_response["result"][0]
