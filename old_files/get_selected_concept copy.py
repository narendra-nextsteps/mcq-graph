"""Get selected concept into the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_selected_concept_query(concept_key):
    """Query for selected concept's dependent concept from db.

    Parameters
    ----------
    concept_key : string
        concept that get selected for getting the dependent concept

    Returns
    -------
    string
        return document of selected concept

    """
    return """
LET concept_key = "{concept_key}"
LET doc = DOCUMENT(CONCAT("{curation_concept_collection}/", concept_key))

RETURN doc
    """.format(
        concept_key=concept_key,
        curation_concept_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def get_selected_concept_query_response(concept_key):
    """Get selected concepts dependent concept from db.

     Parameters
    ----------
    concept_key : string
        concept that get selected for getting the dependent concept

    Returns
    -------
    api_output_pb2.GetSelectedConcept
        return document of selected concept

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_selected_concept_query(
            concept_key
        )
    ).response
    print(query_response)
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
