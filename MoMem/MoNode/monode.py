"""
monode.py
Created on 2023-02-25 4:50:00 PM
Author: Will Selke

The MoNode class is the base dataclass which is the preferred way to stored data in the MoMem NoSQL database.
Its purpose is to stored data along with its metadata. Such as file name, file type, and file size. This allows pictures
to be stored in the database and still be able to be viewed as a picture.
"""
import string
from datetime import datetime
import pickle
import random

from MoMem.config.config import FILE_ID_LENGTH, MONODE_EXTENSION


PADDING_LENGTH = 40
PADDING_LENGTH_SIZE = 10


class MoNode:
    """
    # name : The file name
    # type : The file type (img, txt, video, etc.)

    # data : The file data
    # size : The file size in bytes

    # desc : A description of the file
    # notes : Other details as dictionary
    # tags : A list of tags for the file
    # modi : The date the file was created or last modified
    """

    def __init__(self, name, f_type, data, size = None, description="", notes={}, tags=[], date=None):
        """
        Create a MoNode (SUSSY FUNCTION, USE monode_basic.file_to_monode() INSTEAD)

        :param name: file name and extension
        :param f_type: file type
        :param size: file size in bytes

        :param data: the file data
        :param description: the description of the file

        :param notes: other details as dictionary
        :param tags: the tag of the file
        :param modi: the date the file was created or last modified
        """
        if len(name) > PADDING_LENGTH:
            raise ValueError(f"name is too long {len(name)} > {PADDING_LENGTH}")
        self.name = name

        if len(f_type) > PADDING_LENGTH:
            raise ValueError(f"type is too long {len(f_type)} > {PADDING_LENGTH}")
        self.type = f_type

        if size is None:
            self.size = len(data)
        else:
            self.size = size
        if len(str(self.size)) > PADDING_LENGTH_SIZE:
            raise ValueError(f"size is too long {len(str(self.size))} > {PADDING_LENGTH_SIZE}")

        if date is None:
            self.modi = datetime.now()
        else:
            self.modi = date

        # check if self.modi is too long
        if len(str(self.modi)) > PADDING_LENGTH:
            raise ValueError(f"modi is too long {len(str(self.modi))} > {PADDING_LENGTH}")

        self.desc = description

        self.notes = notes
        self.tags = tags

        self.data = data

    def __str__(self):
        """
        Return the string representation of the MoNode, basically convertion the MoNode to a string

        :return: string representation of the MoNode
        """
        # convert it to a dictionary and dictionary to a string
        # if there is a dictionary in the dictionary, it will be converted to a string
        return str(self.__dict__)

    def pickle(self):
        """
        pickle the MoNode
        the structure of a pickle is:

        first line is the offset key (which contains the byte offset of each element)
        [name, type, size, modi, desc, notes, tags, data]
        second line is the actual pickle data

        :return: the MoNode as a pickle
        """
        # TODO IMPLEMENT ME

        return pickle.dumps(self)

    @staticmethod
    def unpickle(data):
        """
        unpickle the MoNode

        :param data: the pickle data
        :return: the MoNode
        """
        # remove the padding
        data = pickle.loads(data)
        data.name = data.name.strip()
        data.type = data.type.strip()
        data.size = int(data.size)
        data.modi = datetime.strptime(data.modi.strip(), "%Y-%m-%d %H:%M:%S.%f")
        return data

    @staticmethod
    def generate_id():
        """
        Generate a random 15 char string to be used as the file id
        :return: the random string
        """
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(FILE_ID_LENGTH)) + MONODE_EXTENSION
