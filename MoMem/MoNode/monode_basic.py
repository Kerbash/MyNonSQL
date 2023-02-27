"""
monode_basic.py
Created on 2023-02-25 05:21:00 PM
Author: Will Selke

This file contains the basic MoNode class operations, such as save and load.
"""

from .monode import MoNode
from MoMem.config.file_type import file_type
from MoMem.config.config import MONODE_EXTENSION
from MoMem.basic_file_op import base_write, base_read

def file_to_monode(file_name, file_data, desc="", note=None, tags=[], modi=None):
    """
    Convert a file to a MoNode

    :param file_name: the file name
    :param file_data: the file data
    :param desc: the description of the file (optional)
    :param note: other details as dictionary (optional)
    :param tags: the tag of the file (optional)
    :param modi: the modification time of the file (optional)
    :return: the MoNode
    """
    # get the file type
    if note is None:
        note = {}
    file_type_ = file_type[file_name.split(".")[-1]]

    # create the MoNode
    monode = MoNode(name=file_name, data=file_data, description=desc, notes=note, tags=tags, date=modi,
                    f_type=file_type_)

    return monode


def save_as_monode(file_name: str, file_data, database: str, collection: str, desc="", note={}, tags=[]):
    """
    Save a file as a MoNode

    :param file_name: file name and extension
    :param file_data: the data in the file name
    :param database: name of the database
    :param collection: name of the collection
    :param desc: description of the file (optional)
    :param note: additional details as dictionary (optional)
    :param tags: tags for the file (optional)
    """
    # create the MoNode
    monode = file_to_monode(file_name, file_data, desc, note, tags).pickle()
    counter = 0
    while True:
        try:
            ids = MoNode.generate_id()
            # save the MoNode
            base_write(ids, monode, database, collection)
            break
        except FileExistsError:
            print("FIXING")
            counter = counter + 1
            if counter > 10:
                raise FileExistsError("Could not save file after 10 tries (may be a bug)")
            continue


def read_monode(file_id: str, database: str, collection: str):
    """
    Read a MoNode

    :param file_id: the file id
    :param database: name of the database
    :param collection: name of the collection
    :return: the MoNode
    """
    # read the MoNode
    monode = MoNode.unpickle(base_read(file_id + MONODE_EXTENSION, database, collection))

    return monode
