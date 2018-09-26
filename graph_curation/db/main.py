"""For initing the db."""

from .connection import CONNECTION
from . import db_nomenclature as _db_nomenclature


def db_init():
    # """Init the db for the first time."""
    CONNECTION.createDatabase(name=_db_nomenclature.DATABASE)
    graph_db = CONNECTION[_db_nomenclature.DATABASE]
    graph_db.createCollection(name=_db_nomenclature.CHAPTER_COLLECTION)
    graph_db.createCollection(name=_db_nomenclature.CONCEPT_COLLECTION)
    graph_db.createCollection(name=_db_nomenclature.TASK_COLLECTION)
    graph_db.createCollection(name=_db_nomenclature.SUBTASK_COLLECTION)
    graph_db.createCollection(name=_db_nomenclature.USER_COLLECTION)
    graph_db.createCollection(
        name=_db_nomenclature.CURATION_CONCEPTS_COLLETION
    )
    graph_db.createCollection(name=_db_nomenclature.CONCEPT_EDGE_COLLECTION)
    graph_db.createCollection(name=_db_nomenclature.REVOKED_TOKEN_COLLECTION)


if __name__ == "__main__":
    db_init()
