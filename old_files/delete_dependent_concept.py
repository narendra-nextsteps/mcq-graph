"""Updated delete concept in the db"""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def delete_dependent_concept_query(
        concept_key, nested_concept_key, deleted_by
):
    """Query for delete the dependent concept to the concept.

    Parameters
    ----------
    concept_key : string
        concept that deleted from the dependent concept
    nested_concept_key : string
        nested concept key to the concept
    deleted_by : string
        curator that delete the dependent concept

    Returns
    -------
    string
        query to delete the concept into the db

    """
    return """
LET concept_key = "{concept_key}"
LET nested_concept_key = "{nested_concept_key}"
LET deleted_by = "{deleted_by}"
LET doc = DOCUMENT(CONCAT("{curation_concept_collection}/", concept_key))

LET time_deleted = DATE_ISO8601(DATE_NOW())

UPDATE doc WITH {{
    "dependent_concepts": {{
        [nested_concept_key]: MERGE(doc.dependent_concepts[nested_concept_key],
        {{
            "is_active": false,
            "time_deleted": time_deleted
        }})
    }}
}}

IN {curation_concept_collection}
RETURN {{
    is_successful_execution: true
}}
    """.format(
        concept_key=concept_key,
        nested_concept_key=nested_concept_key,
        deleted_by=deleted_by,
        curation_concept_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def delete_dependent_concept_query_response(
        concept_key, nested_concept_key, deleted_by
):
    """Delete dependent concept from concept collection.

     Parameters
    ----------
    concept_key : string
        concept that added the dependent concept
    nested_concept_key : string
        dependent concept name that has to be added to the concept
    deleted_by : string
        curator that delete the dependent concept

    Returns
    -------
    api_output_pb2.Acknowledgement
        return valid execution true or flase

    """
    query_response = _db_objects.graph_db().AQLQuery(
        delete_dependent_concept_query(
            concept_key, nested_concept_key, deleted_by
        )
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
