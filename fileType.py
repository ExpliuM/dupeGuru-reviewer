#!/usr/bin/python3

from enum import Enum

import magic

class TYPES(Enum):
    IMAGE = 1
    VIDEO = 2
    OTHER = 3

def getFileType(fileFullPath):
    mime = magic.from_file(fileFullPath,mime=True) # 'application/pdf'
    if "image" in mime:
        return TYPES.IMAGE
    elif "video" in mime:
        return TYPES.VIDEO
    
    return TYPES.OTHER

