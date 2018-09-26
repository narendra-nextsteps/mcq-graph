"""Add dependent concept to the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def add_dependent_concept_query(
        concept_key, dependent_concept_name, dependent_concept_key, created_by
):
    """Query for add the dependent concept to the concept.

    Parameters
    ----------
    concept_key : string
        concept that added the dependent concept
    dependent_concept_name : string
        dependent concept name that has to be added to the concept
    dependent_concept_key : string
        dependent concept key that has to be added to the concept
    created_by : string
        curator that added the dependent concept

    Returns
    ---------
    string
        query to add dependent concept into the db.

    """
    return """
LET concept_key = "{concept_key}"
LET dependent_concept_name = "{dependent_concept_name}"
LET dependent_concept_key = "{dependent_concept_key}"
LET created_by = "{created_by}"

LET created_time = DATE_ISO8601(DATE_NOW())

LET fn_dependent_concept = {{
    "concept_name": dependent_concept_name,
    "concept_key": dependent_concept_key,
    "created_by": created_by
}}

LET db_dependent_concept = MERGE(fn_dependent_concept, {{
    "time_created": created_time,
    "is_active": true
}})

LET doc = DOCUMENT(CONCAT("{curation_concept_collection}/", concept_key))
UPDATE doc WITH {{
    "dependent_concepts": {{
        [created_time]: db_dependent_concept
    }}
}}

IN {curation_concept_collection}
RETURN {{
    nested_concept_key: created_time,
    dependent_concept: fn_dependent_concept,
    is_successful_execution: true
}}
    """.format(
        concept_key=concept_key,
        dependent_concept_name=dependent_concept_name,
        dependent_concept_key=dependent_concept_key,
        created_by=created_by,
        curation_concept_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def add_dependent_concept_query_response(
        concept_key, dependent_concept_name, dependent_concept_key, created_by
):
    """Added dependent concept to concept collection.

    Parameters
    ----------
    concept_key : string
        concept that added the dependent concept
    dependent_concept_name : string
        dependent concept name that has to be added to the concept
    dependent_concept_key : string
        dependent concept key that has to be added to the concept
    created_by : string
        curator that added the dependent concept

    Returns
    -------
        api_output_pb2.Acknowledgement
        return object of nested_concept_key and dependent concepts

    """
    query_response = _db_objects.graph_db().AQLQuery(
        add_dependent_concept_query(
            concept_key, dependent_concept_name,
            dependent_concept_key, created_by
        )
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
