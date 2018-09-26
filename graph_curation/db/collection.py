"""Methods for Generic Events."""

from google.protobuf import json_format as _json_format

from . import db_objects as _db_objects


def write_to_given_collection(data, collection_name):
    """Write the given data into the db.

    Parameters
    ----------
    data : json
        data that is getting inserted into the db
    collection_name : string
        in which collection data is inserted

    Returns
    -------
    string
        getting key of the document that is inserted

    """
    doc = _db_objects.get_collection(collection_name).createDocument(
        _json_format.MessageToDict(data, preserving_proto_field_name=True)
    )
    if data.HasField('_key'):
        doc._key = data._key
    doc.save()
    return doc._key
