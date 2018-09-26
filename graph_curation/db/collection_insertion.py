# pylint: disable=E0401

"""Data retrival from tables."""
import json
from graph_curation.protos import database_pb2 as _database_pb2
from google.protobuf import json_format as _json_format
from graph_curation.db import collection as _collection
from graph_curation.db import db_nomenclature as _db_nomenclature
from graph_curation.db import db_objects as _db_objects


def insert_chapter_data_using_proto(json_file):
    """Insert chapter data into the chapter document in graph-curation.

    Parameters
    ----------
    json_file : json
        chapters data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        chapter_data = json.load(json_data)
    for chapter in chapter_data:
        proto_collection = _database_pb2.ChaptersDocument()
        data = _json_format.ParseDict(chapter, proto_collection)
        chapter_key = _collection.write_to_given_collection(
            data, _db_nomenclature.CHAPTER_COLLECTION)
    return chapter_key


def insert_revoked_token(revoked_token):
    """Add blacklisted token id to the database.

    Parameters
    ----------
    revoked_token : json object
        add blacklisted token id into the db
    Returns
    -------
    string
        key of the inserted token

    """
    doc = _db_objects.get_collection(
        _db_nomenclature.REVOKED_TOKEN_COLLECTION
    ).createDocument()
    doc._key = revoked_token
    doc.save()
    return doc._key


def insert_concept_data(json_file):
    """Insert chapter data into the chapter document in graph-curation.

    Parameters
    ----------
    json_file : json
        chapters data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        concept_data = json.load(json_data)
    for concept in concept_data:
        data = _json_format.ParseDict(
            concept, _database_pb2.ConceptsDocument()
        )
        concept_key = _collection.write_to_given_collection(
            data, _db_nomenclature.CONCEPT_COLLECTION
        )
    return concept_key


def insert_curation_concept_data(json_file):
    """Insert chapter data into the chapter document in graph-curation.

    Parameters
    ----------
    json_file : json
        chapters data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        concept_data = json.load(json_data)
    for concept in concept_data:
        data = _json_format.ParseDict(
            concept, _database_pb2.ConceptsDocument()
        )
        concept_key = _collection.write_to_given_collection(
            data, _db_nomenclature.CONCEPT_CURATION_COLLETION
        )
    return concept_key


def insert_user_data(json_file):
    """Insert users data into the user document in graph-curation.

    Parameters
    ----------
    json_file : json
        user data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        user_data = json.load(json_data)
    for user in user_data:
        proto_collection = _database_pb2.UsersDocument()
        data = _json_format.ParseDict(
            user, proto_collection)
        user_key = _collection.write_to_given_collection(
            data, _db_nomenclature.USER_COLLECTION
        )
    return user_key


def insert_task_data(json_file):
    """Insert task data into the task document in graph-curation.

    Parameters
    ----------
    json_file : json
        task data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        task_data = json.load(json_data)
    for task in task_data:
        proto_collection = _database_pb2.TasksDocument()
        data = _json_format.ParseDict(
            task, proto_collection)
        task_key = _collection.write_to_given_collection(
            data, _db_nomenclature.TASK_COLLECTION)
    return task_key


def insert_subtask_data(json_file):
    """Insert subtask data into the subtask document in graph-curation.

    Parameters
    ----------
    json_file : json
        subtask data in the json

    Returns
    -------
    string
        key of the document inserted

    """
    with open(json_file) as json_data:
        subtask_data = json.load(json_data)
    for subtask in subtask_data:
        proto_collection = _database_pb2.SubTasksDocument()
        data = _json_format.ParseDict(
            subtask, proto_collection)
        subtask_key = _collection.write_to_given_collection(
            data, _db_nomenclature.SUBTASK_COLLECTION)
    return subtask_key


# insert_subtask_data(
# '/home/anvesha/Documents/Nextsteps/Projects/graph-curation/
# graph_curation/graph_curation/db/Task.json')
