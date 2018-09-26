"""Add unflagged concept into the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def unflagged_dependent_concept_query(
        concept_key, nested_concept_key, unflagged_by
):
    """Query for unflag the dependent concept to the concept.

    Parameters
    ----------
    concept_key : string
        concept that unflagged in the dependent concept
    nested_concept_key : string
        nested concept key to the concept
    unflagged_by : string
        curator that unflag the dependent concept

    Returns
    --------
    string
        add flagged concept into the database

    """
    return """
LET concept_key = "{concept_key}"
LET nested_concept_key = "{nested_concept_key}"
LET unflagged_by = "{unflagged_by}"
LET doc = DOCUMENT(CONCAT("{curation_concept_collection}/", concept_key))

UPDATE doc WITH (
    (doc.dependent_concepts[nested_concept_key].flagged_by != unflagged_by) ?
    {{
        "dependent_concepts": {{
            [nested_concept_key]: MERGE(
                doc.dependent_concepts[nested_concept_key], {{
                "unflagged_by": unflagged_by
            }})
        }}
    }} : {{
        "dependent_concepts": {{
            [nested_concept_key]: MERGE(
                doc.dependent_concepts[nested_concept_key], {{
                "flagged_by": null,
                "unflagged_by": null
            }})
        }}
    }}
)
IN {curation_concept_collection}
RETURN {{
    is_successful_execution: true
}}
    """.format(
        concept_key=concept_key,
        nested_concept_key=nested_concept_key,
        unflagged_by=unflagged_by,
        curation_concept_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def unflagged_dependent_concept_query_response(
        concept_key, nested_concept_key, unflagged_by
):
    """Unflagged dependent concept from conceptcuration collection.

     Parameters
    ----------
    concept_key : string
        concept that unflagged the dependent concept
    nested_concept_key : string
        dependent concept name that has to be added to the concept
    unflagged_by : string
        curator that unflag the dependent concept

    Returns
    -------
    api_output_pb2.Acknowledgement
        return valid execution true or flase

    """
    query_response = _db_objects.graph_db().AQLQuery(
            unflagged_dependent_concept_query(
                concept_key, nested_concept_key, unflagged_by
            )
        ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
