#!/usr/bin/python3
'''metadata file'''

import json
import logging
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
            logging.log(logging.NOTSET, "fileType: %s",  fileType)

            # Handle get meta data by file type
            if fileType is TYPES.IMAGE:
                # Get meta data of image
                logging.log(logging.NOTSET, "filename: %s",  filename)
                try:
                    self.image = Image.open(filename)
                except BaseException:
                    logging.error(
                        "Error occured while loading image file, filename: %s",  filename)

                exifData = self.image.getexif()

                for tagId in exifData:
                    tag = TAGS.get(tagId, tagId)
                    data = exifData.get(tagId)
                    if isinstance(data, bytes):
                        data = data.decode('UTF8', 'replace')
                    # TODO: to improve meta_data we present
                    self.metaData += str(f"{tag:25}\t{data}\n")

                fileSize = os.path.getsize(filename)
                self.metaData += str(f"file size\t\t{fileSize}\n")

                modificationTime = os.path.getmtime(filename)
                self.metaData += str(
                    f"modification time\t{modificationTime}\n")

                changeTime = os.path.getctime(filename)
                self.metaData += str(f"change time\t\t{changeTime}\n")

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
