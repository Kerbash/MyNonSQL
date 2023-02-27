"""
db_col_manage.py ***********************DEPRECATED********************
Created on 2023-02-25 04:59:00 PM
Author: Will Selke

This file contains the functions to list, create, and delete databases and collections.
"""

import os
import MoMem.config.config as cfg

"""=====================================================================================================================
DATABASES
====================================================================================================================="""


def create_database(name):
    """
    Create a database
    :param name: name of the database
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, name)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        raise FileExistsError(f"Database {name} already exists")


def delete_database(name):
    """
    Delete a database
    :param name: name of the database to be deleted
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, name)
    # check if database exists
    if not os.path.exists(path):
        raise FileNotFoundError("The database does not exist")
    # check if the database is empty
    if len(os.listdir(path)) > 0:
        raise OSError("The database is not empty")
    else:
        # delete the folder
        os.removedirs(path)


"""=====================================================================================================================
COLLECTION
====================================================================================================================="""


def create_collection(database, name):
    """
    Create a collection in a database
    :param database: name of the database
    :param name: name of the collection
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, database, name)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        raise FileExistsError(f"Collection {name} already exists in database {database}")


def delete_collection(database, name):
    """
    Delete a collection in a database
    :param database: name of the database
    :param name: name of the collection to be deleted
    """
    DISK = cfg.ROOT_DIR
    path = os.path.join(DISK, database)
    # check if database exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The database {database} does not exist")
    # check if collection exists
    path = os.path.join(path, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"The collection {name} does not exist")
    # check if the collection is empty
    if len(os.listdir(path)) > 0:
        raise OSError("The collection is not empty")
    else:
        # delete the folder
        os.removedirs(path)