"""Add dependent concept."""

import json
# import datetime
from graph_curation.db import db_nomenclature, db_objects


def add_edge_query(edges):
    """Db query.

    Parameters
    ----------
    id : string
        Id to be assigned to new edge.
    fromNode : string
        Id of the concept.
    toNode : string
        Id of the to concept.
    context_id : string
        Id of the context to which the dependent concept has to be added.
    uid : string
        Id of the user who added the dependent concept(edge).

    Returns
    -------
        string
            AQL query

    """
    return """
        FOR edge in {edges}
            INSERT edge IN {McqEdges}
    """.format(
        McqEdges=db_nomenclature.MCQ_EDGE_COLLECTION,
        edges=edges
    )


def add_edge_query_response(edges):
    """Add a dependent concept.

    [description]

    Parameters
    ----------
    id : string
        Id to be assigned to new edge.
    fromNode : string
        Id of the concept.
    toNode : string
        Id of the to concept.
    context_id : string
        Id of the context to which the dependent concept has to be added.
    uid : string
        Id of the user who added the dependent concept(edge).

    Returns
    -------
        object
            returns a success message

    """
    print(edges)
    query_response = db_objects.graph_db().AQLQuery(
        add_edge_query(edges)
    ).response
    if query_response['error']:
        return {"is successful execution": False}
    print(json.dumps(query_response, indent=2))

    return {"is_successful_execution": True}
