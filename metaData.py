#!/usr/bin/python3

from PIL import Image
from PIL.ExifTags import TAGS

from fileType import TYPES, getFileType

import os

class metaData():
    def __init__(self,filename):
      self.metaData=''

      if os.path.exists(filename):
        fileType = getFileType(filename)
        if fileType is TYPES.IMAGE:
            self.image = Image.open(filename)
            exifdata = self.image.getexif()


            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode('UTF8', 'replace')
                self.metaData+=str(f"{tag:25}\t{data}\n")
        elif fileType is TYPES.VIDEO:
            ...
        else:
            ...
      
    def getMetaData(self):
        return self.metaData
