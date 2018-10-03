"""Get assignment data from the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_assignment_data_query():
    """Query users, chapters, tasks in the db.

    Returns
    -------
    dict
        return all users, chapters, tasks.

    """
    return """
        LET chapters = (
            For chapter IN {chapters_collection}
                RETURN {{
                    "chapter_key": chapter._key,
                    "standard": chapter.standard,
                    "chapter": chapter.chapter,
                    "book": chapter.book,
                    "subject": chapter.subject,
                    "chapter_id": chapter.chapter_id
                }}
        )

        LET users = (
            FOR user IN {user_collection}
                RETURN {{
                    "user_key": user._key,
                    "role": user.role
                }}
        )
        RETURN {{
            chapters: chapters,
            users: users
        }}
    """.format(
        user_collection=_db_nomenclature.USER_COLLECTION,
        chapters_collection=_db_nomenclature.CHAPTER_COLLECTION
    )


def get_assignment_data_response():
    """Query all assignment in the db.

    Returns
    -------
    api_output_pb2.GetAllUsers
        return all users username,first name,last name,email.

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_assignment_data_query()
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result'][0]
