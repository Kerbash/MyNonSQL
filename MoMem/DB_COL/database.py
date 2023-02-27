"""
database.py
Created on 2023-02-25 7:22:00 PM
By: Will Selke

This file contains the database class which is a python representation of a database. It contains the functions to
create, delete, and list collections.
"""
import os
from .collection import Collection
import MoMem.config.config as cfg
import MoMem.basic_file_op as bfo


class Database:
    def __init__(self, name, path):
        """
        U SHOULD NOT BE CALLING THIS FUNCTION, USE THE MoMem.find_database() FUNCTION or the MoMem.create_database() FUNCTION
        THIS WILL RESULT IN AN UNDEFINED BEHAVIOR

        Create a database object
        :param name: name of the database
        :param path: path to the database
        """
        self.name = name
        self.path = path

    @staticmethod
    def create_database(name):
        """
        Create a database

        :param name: name of the database
        """
        DISK = cfg.ROOT_DIR
        path = os.path.join(DISK, name)
        if os.path.exists(path):
            raise FileExistsError(f"Database {path} already exists")
        else:
            os.mkdir(path)

        return Database(name, path)

    @staticmethod
    def ls_databases():
        """
        list all databases
        """
        DISK = cfg.ROOT_DIR
        return os.listdir(DISK)

    @staticmethod
    def get_database(name):
        """
        Get a database object
        :param name: name of the database
        :return database: object if it exists, None if it does not
        """
        DISK = cfg.ROOT_DIR
        path = os.path.join(DISK, name)
        if not os.path.exists(path):
            return None
        else:
            return Database(name, path)

    def delete(self):
        """
        Delete the database
        """
        DISK = cfg.ROOT_DIR
        path = os.path.join(DISK, self.name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database {path} does not exist")
        else:
            os.rmdir(path)

    """========================================COLLECTIONS FUNCTIONS========================================="""
    def create_collection(self, name):
        """
        Create a collection in the database
        :param name: name of the collection
        """
        # check if the collection already exists
        path = os.path.join(self.path, name)
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            raise FileExistsError(f"Collection {name} already exists")

        return Collection(name, self.name, path)

    def get_collection(self, name):
        """
        Get a collection object
        :param name: name of the collection
        :return collection: object if it exists, None if it does not
        """
        # check if the collection exists
        path = os.path.join(self.path, name)
        if not os.path.exists(path):
            return None
        else:
            return Collection(name, self.name, path)

    def ls_collections(self):
        """
        List all collections in the database
        :return: list of collections
        """
        return os.listdir(self.path)


