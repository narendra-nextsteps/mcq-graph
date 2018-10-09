"""Query to get text and concepts of the particular context."""

import json
from graph_curation.db import db_nomenclature, db_objects


def sub_task_data_query(context_id):
    """Query to get sub tasks from the db.

    Parameters
    ----------
    context_id : string
        id of the paricular context to curate.

    """
    return """
        LET context_id = "{context_id}"
        FOR content IN {text_content_collection}
            FOR concept in {text_concepts_collection}
                FILTER concept.context_id == context_id
                FILTER content.context_id == context_id
                RETURN {{
                    "_key": concept._key,
                    "clean_text": content.clean_text,
                    "concepts": {{
                        context_id: concept.context_id,
                        dominant_concepts: concept.dominant_concepts
                    }}
                }}
        """.format(
            context_id=context_id,
            text_content_collection=db_nomenclature.TEXT_CONTENT_COLLECTION,
            text_concepts_collection=db_nomenclature.TEXT_CONCEPTS_COLLECTIONS
        )


def sub_task_data_query_response(context_id):
    """Response to api call for subtasks.

    [description]
    Using "text id" a db query is run to get sub tasks on that id.
    """
    query_response = db_objects.graph_db().AQLQuery(
        sub_task_data_query(context_id)
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    print(json.dumps(query_response["result"], indent=2))

    return query_response["result"][0]
