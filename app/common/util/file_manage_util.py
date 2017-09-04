import hashlib
import mimetypes
import time
import os
from app import photos


def get_unique_name(fileIn):
    '''
    返回 md5(filename) + '-' + 时间戳 + 后缀
    :param filename: 
    :return: 
    '''
    image_byte = fileIn.stream.read(8192)
    fileIn.stream.seek(0)
    ext = mimetypes.guess_extension(fileIn.mimetype)
    return '%s-%d%s' % \
           (hashlib.md5(image_byte).hexdigest()[0:16], time.time(), ext)


def get_image_url(image):
    try:
        return photos.url(image)
    except:
        return ''
