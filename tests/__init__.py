#!/usr/bin/python3
"""Testing modules."""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clr_stream(stream: TextIO):
    """Clear given stream

    Args:
        stream (TextIO): stream to clear.
    """
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def del_file(file_path: str):
    """delete file if it exists.
    Args:
        file_path (str): file name.
    """
    if os.path.isfile(file_path):
        os.unlink(file_path)


def res_store(store: FileStorage, file_path='file.json'):
    """Reset given store.
    Args:
        store (FileStorage): FileStorage to reset.
        file_path (str): path to store file.
    """
    with open(file_path, mode='w') as file:
        file.write('{}')
        if store is not None:
            store.reload()


def text_file(file_name):
    """Read given file.

    Args:
        file_name (str): name file.

    Returns:
        str: content of file.
    """
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def wr_text_file(file_name, text):
    """Write text.

    Args:
        file_name (str): file name.
        text (str): content file.
    """
    with open(file_name, mode='w') as file:
        file.write(text)
