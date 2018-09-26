"""Concept curation completion query."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects
# from graph_curation.protos import database_pb2 as _database_pb2


def curation_concept_complete_query(concept_key, chapter_key):
    """Acknowledgement is returned for the completed curation concept.

    Parameters
    ----------
    concept_key : string
        concept that is curated completed

    Returns
    -------
    string
        query for curation concept completion

    """
    return """
LET concept_key="{concept_key}"
LET chapter_key = "{chapter_key}"

LET curated_concept = (
    UPDATE {{ _key: concept_key }} WITH {{
        locked_to: NULL
    }} IN {curation_concpet_collection}
    RETURN NEW
)[0]

LET pending_sub_task = (
    FOR sub_task IN {sub_task_collection}
        FILTER sub_task.concept_key == concept_key
        AND sub_task.status == "PENDING"
        RETURN sub_task
)[0]

LET num_pending_sub_tasks = (
    FOR sub_task in SubTasks
        FILTER sub_task.task_key == pending_sub_task.task_key
        AND sub_task.status == 'PENDING'
        COLLECT WITH COUNT INTO num_pending_sub_tasks
        RETURN num_pending_sub_tasks
)[0]

LET completed_sub_task = (
    UPDATE pending_sub_task WITH {{
        status: "COMPLETED", completed_time: DATE_ISO8601(DATE_NOW())
    }} IN {sub_task_collection}
    RETURN NEW
)[0]


LET is_task_completed = num_pending_sub_tasks == 1

LET completed_task = (
    FILTER is_task_completed
    UPDATE {{ _key: pending_sub_task.task_key }} WITH {{
        status: "COMPLETED", completed_time: DATE_ISO8601(DATE_NOW())
    }} IN {task_collection}
    RETURN NEW
)[0]

LET updated_chapter = (
    FILTER is_task_completed
    UPDATE {{ _key: completed_task.chapter_key }} WITH {{
        locked_to: NULL
    }} In {chapter_collection}
    RETURN NEW
)[0]

RETURN {{
    is_successful_execution: true,
    completed_task: completed_task,
    is_task_completed: is_task_completed
}}
    """.format(
        concept_key=concept_key,
        chapter_key=chapter_key,
        task_collection=_db_nomenclature.TASK_COLLECTION,
        sub_task_collection=_db_nomenclature.SUBTASK_COLLECTION,
        chapter_collection=_db_nomenclature.CHAPTER_COLLECTION,
        curation_concpet_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def assign_newtask_query(completed_task):
    """Acknowledgement is returned for the completed curation concept.

    Parameters
    ----------
    completed_task : dict
        dict of assigned_by,assigned_to..

    Returns
    -------
    string
        query for curation concept completion

    """
    return """
LET completed_task={completed_task}

LET next_user_task = (
    FOR task IN {task_collection}
        FILTER task.chapter_key == completed_task.chapter_key \
        AND task.status == 'NOT_YET_ASSIGNED'
        SORT task._key
        LIMIT 1
        RETURN task
)[0]

LET need_to_create_subtasks = !IS_NULL(next_user_task)

LET updated_next_user_task = (
    FILTER need_to_create_subtasks
    UPDATE next_user_task WITH {{ status: 'PENDING' }} IN {task_collection}
    RETURN NEW
)[0]

LET updated_chapter = (
    FILTER need_to_create_subtasks
    UPDATE {{ _key: completed_task.chapter_key }} WITH {{
        locked_to: updated_next_user_task.assigned_to
    }} In {chapter_collection}
    RETURN NEW
)[0]

LET concepts = (
    FILTER need_to_create_subtasks
    FOR concept_doc in {curation_concpet_collection}
        FILTER POSITION(
            concept_doc.chapter_keys, completed_task.chapter_key
            ) AND IS_NULL(concept_doc.locked_to)
        RETURN {{
            key: concept_doc._key,
            name: concept_doc.concept_name
        }}
)

LET next_user_sub_tasks = (
    FILTER need_to_create_subtasks
    FOR concept in concepts
        INSERT {{
            task_key: next_user_task._key,
            concept_key: concept.key,
            concept_name: concept.name,
            status: 'PENDING',
            assigned_time: DATE_ISO8601(DATE_NOW())
        }} IN {sub_task_collection}
        RETURN NEW
)

LET newly_locked_concepts = (
    FILTER need_to_create_subtasks
    FOR concept in concepts
        UPDATE {{ _key: concept.key }} WITH {{
            locked_to: updated_next_user_task.assigned_to
        }} IN {curation_concpet_collection}
        RETURN {{
            concept_key: concept.key,
            assigned_to: updated_next_user_task.assigned_to
        }}
)

RETURN {{
    is_successful_execution: true
}}
    """.format(
        completed_task=completed_task,
        task_collection=_db_nomenclature.TASK_COLLECTION,
        sub_task_collection=_db_nomenclature.SUBTASK_COLLECTION,
        chapter_collection=_db_nomenclature.CHAPTER_COLLECTION,
        curation_concpet_collection=(
            _db_nomenclature.CURATION_CONCEPTS_COLLETION
        )
    )


def curation_concept_complete_query_response(concept_key, chapter_key):
    """Concept curation complete query response.

    Parameters
    ----------
    concept_key : string
        concept that is curated completed

    Returns
    api_output_pb2.Acknowledgement
        return sucessful execution true  or false when curated concept is
        added in db

    """
    query_response = \
        _db_objects.graph_db().AQLQuery(
            curation_concept_complete_query(
                concept_key, chapter_key
            )
        ).response
    if query_response['result'][0]['is_task_completed']:
        query_response_completed = _db_objects.graph_db().AQLQuery(
            assign_newtask_query(query_response['result'][0]['completed_task'])
        ).response
        print(query_response_completed)
        if query_response_completed['error'] or \
                len(query_response_completed['result']) is 0:
            return {"is_successful_execution": False}
        return query_response_completed['result'][0]
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
