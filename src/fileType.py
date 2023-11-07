#!/usr/bin/python3

from enum import Enum
from magic import MagicException

import logging
import magic

# TODO: Support additional types of files
class TYPES(Enum):
    '''TYPES'''
    IMAGE = 1
    VIDEO = 2
    OTHER = 3


def getFileType(file):
    '''getFileType function'''
    try:
        mime = magic.from_file(file, mime=True)  # 'application/pdf'

        if "image" in mime:
            return TYPES.IMAGE
        elif "video" in mime:
            return TYPES.VIDEO

    except MagicException as e:
        logging.error(e)
    
    return TYPES.OTHER
