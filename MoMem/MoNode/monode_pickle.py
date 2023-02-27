"""
monode_pickle.py
Created on 2023-02-26 9:19:00 PM
By: Will Selke

This file contains the serializer functions for MoMem. These functions serves as an way to pickle and unpickle data
between the MoNode and the file system.
"""
import struct
from datetime import datetime

# Define the max size in byte for the size header of each data type
MAX_DATE_BYTE = 8
MAX_SIZE_DATA_BYTE = 8

# KEY the preceding 2 bytes of the data to determine the type
KEY_CODE = {
    b"mn": "MoNode",
    b"li": "list",
    b"di": "dict",
    b"st": "str",
    b"in": "int",
    b"fl": "float",
    b"dt": "datetime",
    b"by": "byte"
}


def dump(MoNode):
    """
    Pickle the MoNode and return the byte

    :param MoNode: MoNode to pickle
    :return: pickled data
    """
    # create a list from the MoNode
    # In this format
    # [ name, type, size, modified_date, description, notes, tags, data ]
    data = [MoNode.Name, MoNode.Type, MoNode.Size, MoNode.Modi, MoNode.Desc, MoNode.Note, MoNode.Tags, MoNode.Data]

    # serialize the data start 10 because the first 10 are header
    # 2 are the b"mn"
    # and the other 8 are the length of the data
    current_byte = 10
    temp, current_byte = __dump_list(data, current_byte=current_byte)
    output = b"mn" + current_byte.to_bytes(MAX_SIZE_DATA_BYTE, "big") + temp

    return output


def __dump_list(data: list, current_byte=0):
    """
    pickle the list object
    :param data: the list
    :return: byte
    """
    # get the heading size of the list (2 + 8) + 8 (the n elements in the list)
    # and the size of key len(data) * 8
    current_byte += 18 + len(data) * MAX_SIZE_DATA_BYTE
    print("current_byte", current_byte)
    output = b""
    key = []
    for i in data:
        # convert the length to bytes
        key.append(current_byte)
        temp, current_byte = DUMP_FUNCTIONS[type(i)](i, current_byte)
        output += temp

    # compile the output
    # convert the key to bytes
    k_temp = b""
    for k in key:
        k_temp += k.to_bytes(MAX_SIZE_DATA_BYTE, "big")

    output = b"li" + len(output).to_bytes(MAX_SIZE_DATA_BYTE, "big") + \
             len(data).to_bytes(MAX_SIZE_DATA_BYTE, "big") + k_temp + output
    return output, current_byte


def __dump_dict(data: dict, start=0):
    pass


def __dump_str(data: str, current_byte=0):
    """
    pickle the string object
    :param data: string input
    :return: byte string with header
    """
    # convert the string to bytes
    data = data.encode()
    # convert the length to bytes
    data_len = len(data)
    # return the length and the data
    return b"st" + data_len.to_bytes(MAX_SIZE_DATA_BYTE, "big") + data, \
        current_byte + 2 + MAX_SIZE_DATA_BYTE + data_len


def __dump_int(data: int, current_byte=0):
    """
    pickle the int object
    :param data: int input
    :return: byte string with header
    """
    # convert the int to bytes
    data = data.to_bytes(MAX_SIZE_DATA_BYTE, "big")
    # return the data
    return b"in" + data, current_byte + 2 + MAX_SIZE_DATA_BYTE


def __dump_float(data: float, current_byte=0):
    """
    pickle the float object
    :param data: the float
    :return: byte string with header
    """
    # convert the float to bytes
    data = struct.pack('f', data)
    # return the data
    return b"fl" + data, current_byte + 2 + MAX_SIZE_DATA_BYTE


def __dump_datetime(data: datetime, current_byte=0):
    """
    pickle the datetime object
    :param data: datetime input
    :return: byte string with header
    """
    # convert the datetime to bytes
    # NOTE: the d means that its 8 bytes to use double precision
    data = struct.pack('d', data.timestamp())
    # return the data
    return b"dt" + data, current_byte + 2 + MAX_DATE_BYTE


def __dump_bytes(data: bytes, current_byte=0):
    """
    pickle the bytes data
    :param data: the bytes string
    :return: byte string with header attached
    """
    # convert the length to bytes
    data_len = len(data)
    # return the length and the data
    return b"by" + data_len.to_bytes(MAX_SIZE_DATA_BYTE, "big") + data, \
        current_byte + 2 + MAX_SIZE_DATA_BYTE + data_len


DUMP_FUNCTIONS = {
    list: __dump_list,
    dict: __dump_dict,
    str: __dump_str,
    int: __dump_int,
    float: __dump_float,
    datetime: __dump_datetime,
    bytes: __dump_bytes
}
