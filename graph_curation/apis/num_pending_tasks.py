"""Query to get all tasks."""
from graph_curation.db import db_nomenclature, db_objects


def num_pending_tasks(username):
    """Query to get all tasks."""
    return """
        let user  = "{username}"

        let userTasks = (
            for task in Tasks
                filter task.assigned_to == user and task.status == 'PENDING'
                return task
            )

        let userSubTasks = (
            for task in userTasks
                for subTask in SubTasks
                    filter subTask.task_key == task._key and subTask.status == 'PENDING'
                    return subTask
        )

        return {{
            pending_tasks: length(userTasks),
            pending_sub_tasks: length(userSubTasks)
        }}
    """.format(chapters=db_nomenclature.CHAPTER_COLLECTION, username=username)


def num_pending_tasks_response(username):
    """Response to api call for tasks assigned to a user.

    Parameters
    ----------
    uid : strig

    Returns
    -------
    array
        response form the db query for asigned tasks.

    """
    query_response = \
        db_objects.graph_db().AQLQuery(
            num_pending_tasks(username)
        ).response

    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    data = query_response["result"][0]
    print(query_response, data)
    return data
