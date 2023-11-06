#!/usr/bin/python3

from enum import Enum
from magic import MagicException

import logging
import magic

# TODO: Support additional types of files
class TYPES(Enum):
    '''TYPES'''
    IMAGE = 1
    # IMAGE_HEIC = 2 # Future feature
    VIDEO = 3
    OTHER = 4


def getFileType(file):
    '''getFileType function'''
    try:
        mime = magic.from_file(file, mime=True)  # 'application/pdf'

        # if "image/heic" in mime:
        #     return TYPES.IMAGE_HEIC
        if "image" in mime:
            return TYPES.IMAGE
        elif "video" in mime:
            return TYPES.VIDEO

    except MagicException as e:
        logging.error(e)
    
    return TYPES.OTHER
