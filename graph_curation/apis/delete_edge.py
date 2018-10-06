"""Delete a dependent concept."""

import json
import datetime
from graph_curation.db import db_objects, db_nomenclature


def delete_edge_query(edge_id, username):
    """DB Query to delete dependent concept.

    Parameters
    ----------
    edge_id : string
        edge to be deleted.
    username : string
        edge_id of the user who deleted it.
    context_id: string
        context in which the edge has to be deleted.

    Returns
    -------
        string
            AQL Query

    """
    return """
    LET doc = DOCUMENT("{mcq_edge_collection}/{edge_id}")
    UPDATE doc WITH {{
        "deleted_time": "{username}",
        "deleted_by": "{time}"
    }} IN {mcq_edge_collection}
    """.format(
        edge_id=edge_id,
        username=username,
        time=str(datetime.datetime.utcnow().isoformat()),
        mcq_edge_collection=db_nomenclature.VIDEO_EDGE_COLLECTION
    )


def delete_edge_query_response(edge_id, username):
    """Delete the dependent concept(edge).

    Parameters
    ----------
    edge_id : string
        edge to be deleted.
    username : string
        edge_id of the user who deleted it.
    context_id: string
        context in which the edge has to be deleted.

    Returns:
        array
            success message

    """
    query_response = db_objects.graph_db().AQLQuery(
        delete_edge_query(edge_id, username)
    ).response

    if query_response['error']:
        return {"is successful execution": False}

    print(json.dumps(query_response, indent=2))

    return {"is_successful_execution": True}
