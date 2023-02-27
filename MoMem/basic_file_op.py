"""
basic_file_op.py
Created on 2023-02-25 7:46:00 PM
By: Will Selke

This file contains the basic file save / load / read / delete functions for MoMem. These functions serves as an interface between
the MoMem and the file system. This file should not be used directly, instead use the MoMem functions.
"""

import os
import MoMem.config.config as cfg


def base_write(name, data, database, collection, overwrite=False):
    """
    Most basic save function which set the name of the stored file

    :param name: name of the file
    :param data: data to save
    :param database: database to save to
    :param collection: collection to save to
    :param overwrite: overwrite the file or not
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, database)
    # check if database exists
    if not os.path.exists(path):
        raise FileNotFoundError("The database does not exist")

    # check if collection exists
    path = os.path.join(path, collection)
    if not os.path.exists(os.path.dirname(path)):
        raise FileNotFoundError("The collection does not exist")

    # check if file exists
    path = os.path.join(path + "/data", name)
    if not overwrite and os.path.exists(path):
        raise FileExistsError(f"File {path} already exists")

    with open(path, "wb") as f:
        # get the size in bytes of the data
        f.write(data)


def base_read(name, database, collection):
    """
    Most basic read function
    :param name: name of the file
    :param database: name of the database
    :param collection: name of the collection
    :return: data
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, database)
    # check if database exists
    if not os.path.exists(path):
        raise FileNotFoundError("The database does not exist")

    # check if collection exists
    path = os.path.join(path, collection)
    if not os.path.exists(os.path.dirname(path)):
        raise FileNotFoundError("The collection does not exist")

    # check if file exists
    path = os.path.join(path + "/data", name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist")

    with open(path, "rb") as f:
        data = f.read()

    return data


def base_del(name, database, collection):
    """
    Most basic delete function
    :param name: name / id of the file
    :param database: name of the database
    :param collection: name of the collection
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, database, collection + "/data", name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist")
    else:
        os.remove(path)