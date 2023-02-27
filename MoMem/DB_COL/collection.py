"""
collection.py
Created on 2023-02-25 7:29:00 PM
By: Will Selke

This file contains the collection class which is a python representation of a collection. It contains the functions to
create, delete, and list documents.
"""
import os

from MoMem import file_to_monode
from MoMem.config.config import ROOT_DIR
from MoMem.MoNode.monode import MoNode
from MoMem.basic_file_op import base_write, base_del, base_read


class Collection:
    def __init__(self, name, database, path):
        """
        YOU SHOULD NOT BE CALLING THIS FUNCTION, USE THE MoMem.find_collection() FUNCTION or the MoMem.create_collection() FUNCTION
        THIS WILL RESULT IN AN UNDEFINED BEHAVIOR

        Create a collection object
        :param name: name of the collection
        :param database: name of the database
        :param path: path to the collection
        """
        self.name = name
        self.database = database
        self.path = path

        # set up the metadata file
        # create the data folder
        data_p = os.path.join(self.path, "data")
        if not os.path.exists(data_p):
            os.mkdir(data_p)

    def delete(self):
        """
        Delete the collection
        """
        # check if the collection is empty
        if len(os.listdir(self.path + "/data")) > 0:
            raise OSError("The collection is not empty")
        else:
            for root, dirs, files in os.walk(self.path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))

            # delete the collection folder
            os.rmdir(self.path)

            del self

    """========================================DOCUMENTS FUNCTIONS========================================="""

    def ls_documents(self):
        """
        List all documents in the collection (OS FUNCTION)
        :return: list of documents raw name
        """
        return os.listdir(self.path + "/data")

    def save_monode(self, monode: MoNode, id=None, overwrite=False, indexed=False):
        """
        Add a monode to the collection

        :param monode: monode to be added
        :param id: id of the monode when saved to file (if None, a random id will be generated)
        :param overwrite: whether to overwrite the monode if it already exists\
        :param indexed: whether to index the monode to the collection
        """
        # in the case of no id provided, keep generating ids until a unique one is found
        if id is None:
            id = MoNode.generate_id()
            while os.path.exists(os.path.join(self.path + "/data", id)):
                id = MoNode.generate_id()

        # save the MoNode
        base_write(id, monode.pickle(), self.database, self.name, overwrite=overwrite)

    def save_file_as_monode(self, file_name, file_data, id=None, desc="", notes={}, tags=[], modi=None, overwrite=False,
                            indexed=False):
        """
        Save a file as a monode
        :param indexed:
        :param overwrite:
        :param file_name: name of the file
        :param file_data: data of the file
        :param id: id of the monode when saved to file (if None, a random id will be generated)
        :param desc: description of the file
        :param notes: other details as dictionary
        :param tags: tags of the file
        :param modi: date the file was created or last modified
        :param overwrite: whether to overwrite the monode if it already exists
        :param indexed: whether to index the monode
        """
        # create a monode
        monode = file_to_monode(file_name, file_data, desc, notes, tags)

        # save the monode
        self.save_monode(monode, id, overwrite, indexed)

    def get_monode(self, id):
        """
        Get a monode from the collection
        :param id: id of the monode
        :return: the monode
        """
        monode = base_read(id, self.database, self.name)
        return MoNode.unpickle(monode)

    def del_monode(self, id):
        """
        Delete a file from a collection (Should only be called by the collection class)

        :param name: name of the file
        :param collection: collection to delete from
        """
        base_del(id, self.database, self.name)

    """========================================INDEXING FUNCTIONS========================================="""
    def create_index(self, field, type=None):
        """
        create an index for a collection using field as the key
        :param collection: the collection to index
        :param field: the field to index
        :param type: type of index
        """
        # get all current documents
        documents = self.ls_documents()

        # do this on a different thread as it may take a while
        # TODO IMPLEMENT THIS ON A SEPERATE THREAD
