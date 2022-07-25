#!/usr/bin/python3

from PIL import Image
from PIL.ExifTags import TAGS

import os

class ImageMetaData():
    def __init__(self,filename):
      self.metaData=''
      if os.path.exists(filename):
        self.image = Image.open(filename)

        exifdata = self.image.getexif()


        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode('UTF8', 'replace')
            self.metaData+=str(f"{tag:25}\t{data}\n")
      
    def getMetaData(self):
        return self.metaData
          
def main():
  imageMetaData = ImageMetaData('/Users/explium/OneDrive - Technion/Pictures/Miscellaneous/Alex/2013-September-Thailand/20130907_090348 (1).jpg')
  print(imageMetaData.getMetaData())
  
if __name__ == '__main__':
    main()
