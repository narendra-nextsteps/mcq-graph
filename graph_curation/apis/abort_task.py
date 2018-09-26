"""Abort task query."""
from graph_curation.db import db_objects as _db_objects


def abort_transaction_function(chapter_key, username):
    """Acknowledgement is returned when task is aborted.

    Parameters
    ----------
    chapter_key : string
        which chapter is getting aborted
    username : string
        for which user task is aborted
    Returns
    -------
    string
        query for abort a task.

    """
    return """
function() {
    let chapterKey = "%s", username = "%s"
    let db = require('@arangodb').db
    console.log(chapterKey, username)
    let abortTaskExecution = db._query(`
LET chapter_key = @chapter_key
LET username = @username

LET aborted_task = (
    FOR task in Tasks
        FILTER task.chapter_key == chapter_key AND task.status == "PENDING"
        AND task.assigned_to == username
        UPDATE task WITH {
            status: "ABORTED"
        } IN Tasks
        RETURN NEW
)[0]

LET aborted_sub_tasks = (
    FOR subtask in SubTasks
        FILTER subtask.task_key == aborted_task._key
        UPDATE subtask WITH {
            status: "ABORTED"
        } IN SubTasks
        RETURN NEW
)

LET concepts_locked_to_aborted_task = (
    FOR aborted_sub_task in aborted_sub_tasks
        UPDATE { _key: aborted_sub_task.concept_key } WITH {
            locked_to: NULL
        } IN CurationConcepts
        RETURN NEW
)

LET aborted_chapter = (
    UPDATE { _key: chapter_key } WITH {
        locked_to: NULL
    } IN Chapters
    RETURN NEW
)[0]

RETURN {
    aborted_task: aborted_task,
    aborted_sub_tasks: aborted_sub_tasks,
    aborted_chapter: aborted_chapter,
    concepts_locked_to_aborted_task: concepts_locked_to_aborted_task
}
    `, {chapter_key: chapterKey, username: username}).toArray()[0]

    console.log(abortTaskExecution)

    let assignNextUserExecution = db._query(`
LET aborted_task = @aborted_task

LET next_user_task = (
    FOR task IN Tasks
        FILTER task.chapter_key == aborted_task.chapter_key
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
    UPDATE { _key: aborted_task.chapter_key } WITH {
        locked_to: updated_next_user_task.assigned_to
    } In Chapters
    RETURN NEW
)[0]

LET newly_locked_concepts = (
    FILTER need_to_create_subtasks
    FOR concept_doc in CurationConcepts
        FILTER POSITION(concept_doc.chapter_keys, aborted_task.chapter_key)
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
} `, {aborted_task: abortTaskExecution.aborted_task}).toArray()[0]

    console.log(assignNextUserExecution)

    return {
        aborted_task: abortTaskExecution.aborted_task,
        aborted_sub_tasks: abortTaskExecution.aborted_sub_tasks,
        aborted_chapter: abortTaskExecution.aborted_chapter,
        concepts_locked_to_aborted_task:
            abortTaskExecution.concepts_locked_to_aborted_task,
        updated_next_user_task: assignNextUserExecution.updated_next_user_task,
        updated_chapter: assignNextUserExecution.updated_chapter,
        need_to_create_subtasks:
            assignNextUserExecution.need_to_create_subtasks,
        next_user_sub_tasks: assignNextUserExecution.next_user_sub_tasks,
        newly_locked_concepts: assignNextUserExecution.newly_locked_concepts,
        is_successful_execution: true
    }
}
""" % (chapter_key, username)


def abort_task_query_response(chapter_key, username):
    """Abort task query response.

    Parameters
    ----------
    chapter_key : string
        which chapter is getting aborted
    username : string
        for which user task is aborted

    Returns
    api_output_pb2.Acknowledgement
        return sucessful execution true or false when task is aborted

    """
    query_response = _db_objects.graph_db().transaction({
        "write": ["Tasks", "SubTasks", "CurationConcepts", "Chapters"],
        "read": ["Tasks", "SubTasks", "CurationConcepts"]
        }, abort_transaction_function(chapter_key, username))
    if query_response['error']:
        return {"is_successful_execution": False}
    return query_response['result']
