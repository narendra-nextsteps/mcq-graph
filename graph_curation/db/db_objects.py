"""All the objects that communicate with DB."""

from .connection import CONNECTION
from . import db_nomenclature as _db_nomenclature


def get_collection(collection_name):
    """Get the collection for the given collection name.

    Parameters
    ----------
    collection_name : string
        name of the collection

    Returns
    -------
    pyArango.collection.Collection
        collection object of the given collection name.

    """
    return graph_db()[collection_name]


def graph_db():
    """Return connection to db.

    Returns
    -------
    pyArango.database.Database
        database object.

    """
    return CONNECTION[_db_nomenclature.DATABASE]
