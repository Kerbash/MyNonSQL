"""
monode_pickle.py
Created on 2023-02-26 9:19:00 PM
By: Will Selke

This file contains the serializer functions for MoMem. These functions serves as an way to pickle and unpickle data
between the MoNode and the file system.
"""
import struct
from datetime import datetime
from typing import Tuple, List, Any

from MoMem import MoNode

# Define the max size in byte for the size header of each data type
MAX_DATE_BYTE = 8
MAX_SIZE_DATA_BYTE = 8

# KEY the preceding 2 bytes of the data to determine the type
KEY_CODE = {
    b"mn": MoNode,
    b"li": list,
    b"di": dict,
    b"st": str,
    b"in": int,
    b"fl": float,
    b"dt": datetime,
    b"by": bytes
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
    data = [MoNode.name, MoNode.type, MoNode.size, MoNode.modi, MoNode.desc, MoNode.notes, MoNode.tags, MoNode.data]

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
    current_byte += 10
    prev_byte = current_byte
    current_byte += 8 # the n-elements in the list is 8 bytes long
    current_byte += len(data) * 8 # the key is 8 bytes long for each element
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
    output = b"li" + (current_byte - prev_byte).to_bytes(MAX_SIZE_DATA_BYTE, "big") + \
             len(data).to_bytes(MAX_SIZE_DATA_BYTE, "big") + k_temp + output

    return output, current_byte


def __dump_dict(data: dict, current_byte=0):
    """
    pickle the dict object
    :param data: the dict
    :param start: where to start the byte counter
    :return: byte string with header
    """
    # convert the dict to a list
    # TODO Come up with a better way to pickle the dict
    # TODO WAY TO TIRED TO THINK RIGHT NOW 2023-02-26 10:58:00 PM
    items = data.items()
    outlist = []

    # create a list of the keys and values
    for item in items:
        outlist.append(item[0])
        outlist.append(item[1])

    # pickle the list
    outlist, current_byte = __dump_list(outlist, current_byte)
    return b"di" + outlist, current_byte


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


def load(data):
    """
    Load the data from the byte string of the pickled data

    :param data: the byte string to be loaded
    :return: MoNode object
    """
    # verify the type
    if type(data) != bytes:
        raise TypeError("data must be a byte string")

    # verify the header
    if data[:2] != b"mn":
        raise ValueError("This is not a MoNode byte string")

    # get the length of the data
    data_len = int.from_bytes(data[2:10], "big")

    outlist = []

    # get the number of elements in the list
    data = data[10:]
    output, _ = __load_list(data)

    # create a MoNode object from the list
    return MoNode(name=output[0], f_type=output[1], size=output[2], date=output[3], description=output[4],
                  notes=output[5], tags=output[6], data=output[7])


def __load_list(data) -> tuple[list[Any], bytes]:
    """
    Load the list object from pickled data
    must start with "li"
    :param data: the pickled data
    :return: the list and the remaining data
    """
    # verify the header
    if data[:2] != b"li":
        raise ValueError("This is not a list byte string")

    output = []
    # get the length of the data
    data_len = int.from_bytes(data[2:10], "big")
    # trim the data
    list_data = data[10:data_len + 10]
    # get the number of elements in the list
    num_elements = int.from_bytes(list_data[:8], "big")
    # remove the key portion of the data
    list_data = list_data[8 + num_elements * MAX_SIZE_DATA_BYTE:]


    for n in range(num_elements):
        # get the type of the first element
        data_type = list_data[:2]
        # get the function to load the data
        n_ele, list_data = LOAD_FUNCTIONS[KEY_CODE[data_type]](list_data)
        output.append(n_ele)

    return output, data[10 + data_len:]


def __load_dict(data) -> tuple[dict, bytes]:
    """
    load the dict object from pickled data
    :param data: the pickled data
    :return: the dict
    """
    # TODO CHANGE THIS TO BE MORE EFFICIENT LOOK AT __dump_dict
    # verify the header
    if data[:2] != b"di":
        raise ValueError(f"This is not a dict byte string {data[:2]}")

    # remove the header and get list back
    data = data[2:]
    l, data = __load_list(data)

    output = {}

    # check integrity of the list to dict
    if len(l) % 2 != 0:
        raise ValueError("The list is not a valid dict")
    else:
        for i in range(int(len(l) / 2)):
            output[l[2 * i]] = l[2 * i + 1]

    return output, data


def __load_str(data) -> tuple[str, bytes]:
    """
    Load the string object from pickled data
    :param data: the pickled data
    :return: the string
    """
    # verify the header
    if data[:2] != b"st":
        raise ValueError("This is not a string byte string")
    # get the length of the data
    data_len = int.from_bytes(data[2:10], "big")
    # return the data
    return data[10:10 + data_len].decode(), data[10 + data_len:]


def __load_int(data) -> tuple[int, bytes]:
    """
    Load the int object from pickled data
    :param data: the pickled data
    :return: the int
    """
    # verify the header
    if data[:2] != b"in":
        raise ValueError("This is not an int byte string")

    # return the data
    return int.from_bytes(data[2:10], "big"), data[10:]


def __load_float(data) -> tuple[float, bytes]:
    """
    Load the float object from pickled data
    :param data: the pickled data
    :return: the float
    """
    # verify the header
    if data[:2] != b"fl":
        raise ValueError("This is not a float byte string")

    # return the data
    return struct.unpack('f', data[2:10])[0], data[10:]


def __load_datetime(data) -> tuple[datetime, bytes]:
    """
    Load the datetime object from pickled data
    :param data: the pickled data
    :return: the datetime
    """
    # verify the header
    if data[:2] != b"dt":
        raise ValueError("This is not a datetime byte string")

    # return the data
    return datetime.fromtimestamp(struct.unpack('d', data[2:10])[0]), data[10:]


def __load_bytes(data) -> tuple[bytes, bytes]:
    """
    Load the bytes object from pickled data
    :param data: the pickled data
    :return: the bytes
    """
    # verify the header
    if data[:2] != b"by":
        raise ValueError("This is not a bytes byte string")

    # get the length of the data
    data_len = int.from_bytes(data[2:10], "big")
    # return the data
    return data[10:10 + data_len], data[10 + data_len:]


LOAD_FUNCTIONS = {
    list: __load_list,
    dict: __load_dict,
    str: __load_str,
    int: __load_int,
    float: __load_float,
    datetime: __load_datetime,
    bytes: __load_bytes
}
