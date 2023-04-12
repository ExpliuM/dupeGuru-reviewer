#!/usr/bin/python3


# from ffprobe import FFProbe
from PIL import Image
from PIL.ExifTags import TAGS

import ffmpeg
import json
import os

from fileType import TYPES, getFileType


class metaData():
    def __init__(self, filename):
        self.metaData = ''

        if os.path.exists(filename):
            # Get file type
            fileType = getFileType(filename)

            # Handle get meta data by file type
            if fileType is TYPES.IMAGE:
                # Get meta data of image
                self.image = Image.open(filename)
                exifdata = self.image.getexif()

                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    if isinstance(data, bytes):
                        data = data.decode('UTF8', 'replace')
                    self.metaData += str(f"{tag:25}\t{data}\n")

            elif fileType is TYPES.VIDEO:
                # Get meta data of video
                vidMetaData = ffmpeg.probe(filename)

                # self.metaData += str(f"{vidMetaData.metadata.__str__}\t{data}\n")
                self.metaData += json.dumps(vidMetaData,indent=1)
            else:
                ...

    def getMetaData(self):
        return self.metaData
