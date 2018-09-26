"""Model for dependent concepts."""

import json
from graph_curation.db import db_nomenclature, db_objects


def dependent_concepts_query(concept_id, mcq_id):
    """Db query.

    Parameters
    ----------
    concept_id : string
        The id of the main concept for which the dependents has to be get.
    mcq_id : string
        The id of the paragraph or the context (eg: heading ) from which the
        main concept has to be selected.

    Returns
    -------
        string
            AQL query

    """
    return """
        FOR edge IN {McqEdges}
            filter edge.mcq_id == "{mcqId}" \
            AND edge._from == "{fromNode}"
            RETURN edge
    """.format(
        McqEdges=db_nomenclature.MCQ_EDGE_COLLECTION,
        mcqId=mcq_id,
        fromNode=concept_id
    )


def dependent_concepts_query_response(concept_id, mcq_id):
    """Get the dependent concepts for given concept
    in the given context(mcq_id).

    Parameters
    ----------
    concept_id : string
        The id of the main concept for which the dependents has to be get.
    mcq_id : string
        The id of the paragraph or the context (eg: heading ) from which the
        main concept has to be selected.

    Returns
    -------
        array
            array of object with edges.


    """
    query_response = db_objects.graph_db().AQLQuery(
        dependent_concepts_query(concept_id, mcq_id)
    ).response
    if query_response['error']:
        return {"is successful execution": False}
    elif len(query_response['result']) is 0:
        return {"is_successful_execution": True, "dependent_concepts": []}
    print(json.dumps(query_response["result"][0], indent=2))
    dependent_concepts = {"dependent_concepts": query_response["result"]}
    print("=================")
    print(json.dumps(dependent_concepts, indent=2))
    return dependent_concepts
