"""Complete sub task or task query."""
from graph_curation.db import db_objects as _db_objects


def complete_transaction_function(chapter_key, concept_key):
    """Acknowledgement is returned when sub task is completed.

    Parameters
    ----------
    chapter_key : string
        which chapter is getting completed
    concept_key : string
        for which concept key subtask is completed
    Returns
    -------
    string
        query for complete a sub task.

    """
    return """
function() {
    let chapterKey = "%s", conceptKey = "%s"
    let db = require('@arangodb').db

    let completeTaskExecution = db._query(`
LET chapter_key = @chapter_key
LET concept_key = @concept_key

LET curated_concept = (
    UPDATE { _key: concept_key } WITH {
        locked_to: NULL
    } IN CurationConcepts
    RETURN NEW
)[0]

LET pending_sub_task = (
    FOR sub_task IN SubTasks
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
    UPDATE pending_sub_task WITH {
        status: "COMPLETED", completed_time: DATE_ISO8601(DATE_NOW())
    } IN SubTasks
    RETURN NEW
)[0]


LET is_task_completed = num_pending_sub_tasks == 1

LET completed_task = (
    FILTER is_task_completed
    UPDATE { _key: pending_sub_task.task_key } WITH {
        status: "COMPLETED", completed_time: DATE_ISO8601(DATE_NOW())
    } IN Tasks
    RETURN NEW
)[0]

LET updated_chapter = (
    FILTER is_task_completed
    UPDATE { _key: completed_task.chapter_key } WITH {
        locked_to: NULL
    } In Chapters
    RETURN NEW
)[0]

RETURN {
    curated_concept: curated_concept,
    completed_sub_task: completed_sub_task,
    is_task_completed: is_task_completed,
    completed_task: completed_task,
    updated_chapter: updated_chapter
}

    `, {chapter_key: chapterKey, concept_key: conceptKey}).toArray()[0]

    console.log(completeTaskExecution)

    let assignNextUserExecution = db._query(`
LET completed_task = @completed_task

LET next_user_task = (
    FOR task IN Tasks
        FILTER task.chapter_key == completed_task.chapter_key
        AND task.status == 'NOT_YET_ASSIGNED'
        SORT task._key
        LIMIT 1
        RETURN task
)[0]

LET need_to_create_subtasks = !IS_NULL(next_user_task)

LET updated_next_user_task = (
    FILTER need_to_create_subtasks
    UPDATE next_user_task WITH { status: 'PENDING' } IN Tasks
    RETURN NEW
)[0]

LET updated_chapter = (
    FILTER need_to_create_subtasks
    UPDATE { _key: completed_task.chapter_key } WITH {
        locked_to: updated_next_user_task.assigned_to
    } In Chapters
    RETURN NEW
)[0]

LET newly_locked_concepts = (
    FILTER need_to_create_subtasks
    FOR concept_doc in CurationConcepts
        FILTER POSITION(concept_doc.chapter_keys, completed_task.chapter_key)
        AND IS_NULL(concept_doc.locked_to)
        UPDATE concept_doc WITH {
            locked_to: updated_next_user_task.assigned_to
        } IN CurationConcepts
        RETURN {
            key: concept_doc._key,
            name: concept_doc.concept_name,
            assigned_to: updated_next_user_task.assigned_to
        }
)

LET next_user_sub_tasks = (
    FILTER need_to_create_subtasks
    FOR concept in newly_locked_concepts
        INSERT {
            task_key: next_user_task._key,
            concept_key: concept.key,
            concept_name: concept.name,
            status: 'PENDING',
            assigned_time: DATE_ISO8601(DATE_NOW())
        } IN SubTasks
        RETURN NEW
)

RETURN {
    updated_next_user_task: updated_next_user_task,
    updated_chapter: updated_chapter,
    need_to_create_subtasks: need_to_create_subtasks,
    next_user_sub_tasks: next_user_sub_tasks,
    newly_locked_concepts: newly_locked_concepts
} `, {completed_task: completeTaskExecution.completed_task}).toArray()[0]
    if (completeTaskExecution.is_task_completed) return assignNextUserExecution

    console.log(assignNextUserExecution)

    return {
        completed_task: completeTaskExecution.completed_task,
        complte_sub_tasks: completeTaskExecution.completed_sub_task,
        completed_chapter: completeTaskExecution.updated_chapter,
        updated_next_user_task: assignNextUserExecution.updated_next_user_task,
        updated_chapter: assignNextUserExecution.updated_chapter,
        need_to_create_subtasks:
        assignNextUserExecution.need_to_create_subtasks,
        next_user_sub_tasks: assignNextUserExecution.next_user_sub_tasks,
        newly_locked_concepts: assignNextUserExecution.newly_locked_concepts,
        is_successful_execution: true
    }
}
""" % (chapter_key, concept_key)


def complete_task_query_response(chapter_key, concept_key):
    """Complete task query response.

    Parameters
    ----------
    chapter_key : string
        which chapter is getting completed
    concept_key : string
        for which concept key subtask is completed

    Returns
    api_output_pb2.Acknowledgement
        return sucessful execution true or false when task is completed

    """
    query_response = _db_objects.graph_db().transaction({
        "write": ["Tasks", "SubTasks", "CurationConcepts", "Chapters"],
        "read": ["Tasks", "SubTasks", "CurationConcepts"]
        }, complete_transaction_function(chapter_key, concept_key))
    print(query_response)
    if query_response['error']:
        return {"is_successful_execution": False}
    return query_response['result']
