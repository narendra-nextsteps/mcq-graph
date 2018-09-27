"""Delete a dependent concept."""

import json
import datetime
from graph_curation.db import db_objects


def delete_edge_query(edge_id, uid):
    """DB Query to delete dependent concept.

    Parameters
    ----------
    edge_id : string
        edge to be deleted.
    uid : string
        edge_id of the user who deleted it.
    context_id: string
        context in which the edge has to be deleted.

    Returns
    -------
        string
            AQL Query

    """
    return """
        for edge in McqEdges
            filter edge._key == "{edge_id}"
            update edge with {{
                "deleted_by": "{uid}",
                "deleted_time": "{time}"
                }} in McqEdges
    """.format(
        edge_id=edge_id,
        uid=uid,
        time=str(datetime.datetime.utcnow().isoformat())
    )


def delete_edge_query_response(edge_id, uid):
    """Delete the dependent concept(edge).

    Parameters
    ----------
    edge_id : string
        edge to be deleted.
    uid : string
        edge_id of the user who deleted it.
    context_id: string
        context in which the edge has to be deleted.

    Returns:
        array
            success message

    """
    query_response = db_objects.graph_db().AQLQuery(
        delete_edge_query(edge_id, uid)
    ).response

    if query_response['error']:
        return {"is successful execution": False}

    print(json.dumps(query_response, indent=2))

    return {"is_successful_execution": True}
