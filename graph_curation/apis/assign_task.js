`LET assigned_by = "nextsteps"
LET assigned_to_list = ["narendra", "anvesha"]
LET chapter_key = "2344733"
LET num_one_less_assigned_to = LENGTH(assigned_to_list) - 1

LET chapter_doc = DOCUMENT(CONCAT("Chapters/", chapter_key))
LET is_previously_locked = !IS_NULL(chapter_doc.locked_to)

LET tasks = (
    FOR assigned_to_pos in 0..num_one_less_assigned_to
        FILTER assigned_to_list[assigned_to_pos] != chapter_doc.locked_to
        INSERT {
            status: assigned_to_pos == 0 ? (
                is_previously_locked ? 'NOT_YET_ASSIGNED' : 'PENDING'
            ) : 'NOT_YET_ASSIGNED',
            assigned_to: assigned_to_list[assigned_to_pos],
            assigned_by: assigned_by,
            chapter_key: chapter_key,
            chapter: chapter_doc.chapter,
            assigned_time: DATE_ISO8601(DATE_NOW())
        } IN Tasks
        RETURN NEW
)

LET updated_chapter_doc = (
    FILTER IS_NULL(chapter_doc.locked_to)
    UPDATE chapter_doc WITH {
        locked_to: assigned_to_list[0]
    } IN Chapters
    RETURN NEW
)

LET concepts = (
    FOR concept_doc in CurationConcepts
        FILTER POSITION(
            concept_doc.chapter_keys, chapter_key
        ) and IS_NULL(concept_doc.locked_to)
        RETURN {
            key: concept_doc._key,
            name: concept_doc.concept_name
        }
)

LET need_to_create_subtasks = tasks[0].status == 'PENDING'

LET sub_tasks = (
    FILTER need_to_create_subtasks
    FOR concept in concepts
        INSERT {
            task_key: tasks[0]._key,
            concept_key: concept.key,
            concept_name: concept.name,
            status: 'PENDING',
            assigned_time: DATE_ISO8601(DATE_NOW())
        } IN SubTasks
        RETURN NEW
)

LET locked_concepts = (
    FILTER need_to_create_subtasks
    FOR concept in concepts
        UPDATE { _key: concept.key } WITH {
            locked_to: assigned_to_list[0]
        } IN CurationConcepts
        RETURN {
            concept_key: concept.key,
            assigned_to: assigned_to_list[0]
        }
    )

RETURN {
    is_successful_execution: true
}`
