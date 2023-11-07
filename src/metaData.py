#!/usr/bin/python3
'''metadata file'''

import json
import os

import ffmpeg

from pillow_heif import register_heif_opener

from PIL import Image
from PIL.ExifTags import TAGS

from src.fileType import TYPES, getFileType


register_heif_opener()


# TODO: To consider not to use class here
class MetaData():
    '''MetaData class'''

    def __init__(self, filename):
        self.metaData = ''

        if os.path.exists(filename):
            # Get file type
            fileType = getFileType(filename)

            # Handle get meta data by file type
            if fileType is TYPES.IMAGE:
                # Get meta data of image
                self.image = Image.open(filename)
                exifData = self.image.getexif()

                for tagId in exifData:
                    tag = TAGS.get(tagId, tagId)
                    data = exifData.get(tagId)
                    if isinstance(data, bytes):
                        data = data.decode('UTF8', 'replace')
                    # TODO: to improve meta_data we present
                    self.metaData += str(f"{tag:25}\t{data}\n")

            elif fileType is TYPES.VIDEO:
                # Get meta data of video
                videosMetaData = ffmpeg.probe(filename)

                # TODO: To filter out only the relevant fields
                self.metaData += json.dumps(videosMetaData, indent=1)
            else:
                pass

    def getMetaData(self):
        '''Unnecessary parens after 'if' keyword method'''
        return self.metaData
