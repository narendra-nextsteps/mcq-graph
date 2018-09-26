"""Get selection data from the db."""
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def get_selection_data_query(username):
    """Get all the chapters,concepts of the document.

    Parameters
    ----------
    username : string

    Returns
    -------
    string
        return query to get the selection data

    """
    return """
LET username = "{username}"

FOR task_doc in {task_collection}
FILTER task_doc.assigned_to == username AND task_doc.status == "PENDING"
RETURN {{
    "chapter_doc": DOCUMENT(CONCAT("{chapter_collection}/",
    task_doc.chapter_key)),
    "concepts": (
        FOR sub_task_doc in {subtask_collection}
            FILTER sub_task_doc.task_key == task_doc._key AND
            sub_task_doc.status == "PENDING"
            RETURN {{
                "concept_name": sub_task_doc.concept_name,
                "concept_key": sub_task_doc.concept_key
            }}
    )
}}

    """.format(
        username=username,
        task_collection=_db_nomenclature.TASK_COLLECTION,
        subtask_collection=_db_nomenclature.SUBTASK_COLLECTION,
        chapter_collection=_db_nomenclature.CHAPTER_COLLECTION,
    )


def get_selection_data_query_response(username):
    """Get all the chapters,concepts of the document.

    Parameters
    ----------
    username : string
        username for which getting the data

    Returns
    -------
    dict
        return document of selected concept

    """
    query_response = _db_objects.graph_db().AQLQuery(
        get_selection_data_query(
            username
        )
    ).response
    if query_response['error'] or len(query_response['result']) is 0:
        return {"is_successful_execution": False}
    return query_response['result']


def get_selection_data_result(username):
    """Convert data into the format of selection data proto.

    Parameters
    ----------
    username : string
        username for which getting the data

    Returns
    -------
    api_output_pb2.GetSelectionData
        return document of selected concept according to the proto.

    """
    selection_data = get_selection_data_query_response(username)
    print(selection_data)
    concept_data = []
    chapters_data = {}
    final_selection_data = []
    for data in selection_data:
        if data['chapter_doc'] is not None:
            chapters_data = {}
            print("@@@@@@@@@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!!!!!!!!!!!!")
            concept_data = data['concepts']
            chapter_details = data['chapter_doc']
            chapters_data['standard'] = chapter_details['standard']
            chapters_data['subjects'] = []
            subject = {}
            subject['name'] = chapter_details['subject']
            subject['chapters'] = []
            chapter = {}
            chapter['name'] = chapter_details['chapter']
            chapter['concepts'] = []
            if concept_data:
                for concept_name in concept_data:
                    concept = {}
                    concept['concept_name'] = concept_name['concept_name']
                    concept['concept_id'] = concept_name['concept_key']
                    chapter['concepts'].append(concept)
            print("@@@@@@@@@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(concept_data)
            subject['chapters'].append(chapter)
            print(subject)
            print("frgrgrjhbihuygtfrder56t789!!!!!!!!!!!!!!!!!!!!!!!!!!")
            chapters_data['subjects'].append(subject)
            final_selection_data.append(chapters_data)
    return final_selection_data
