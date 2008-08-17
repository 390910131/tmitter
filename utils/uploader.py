# -*- coding: utf-8 -*-
# ## ## ## ## ## ## ## ## ##
# upload file library
# ## ## ## ## ## ## ## ## ##
import sys,os
import time
from StringIO import StringIO
from PIL import Image
from tmitter.settings import *
import ImageFilter

def upload_face(data):
    u"""
    summary:
        Upload user face    
    params:
        data    object  request.FILES.get('uploadcontrolname')
    returns:
        _state  directory {'success':True|False ,'message':error info|new file path}
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    _state = {
        'success' : False,
        'message' : '',
    }
    
    if data.size > 0:
        # try:
        base_im = Image.open(data)        

        size16 = (16,16)
        size24 = (24,24)
        size32 = (32,32)
        size100 = (75,75)

        size_array = (size100,size32,size24,size16)

        # generate file name and the file path
        file_name = time.strftime('%H%M%S') + '.png'
        file_root_path = '%sface/' % (MEDIA_ROOT)
        file_sub_path = '%s' % (str(time.strftime("%Y/%m/%d/")))

        # make different sizes photos
        for size in size_array:
            file_middle_path = '%d/' % size[0]

            file_path = os.path.abspath(file_root_path + file_middle_path + file_sub_path)

            im = base_im
            im = make_thumb(im,size[0])

            # check path exist
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            im.save('%s/%s' % (file_path,file_name),'PNG')


        _state['success'] = True
        _state['message'] = file_sub_path + file_name
        #except:
        #    _state['success'] = False
        #    _state['message'] = '上传头像时出错。'
    else:
        _state['success'] = False
        _state['message'] = '还未选择要上传的文件。'
        
    return _state

def make_thumb(im, size=75):
    u"""
    summary:
        缩略图生成程序
    params:
        sizes   参数传递要生成的尺寸，可以生成多种尺寸
    author:
        Neil Chen
    """
            
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)            
        region = im.crop(box)

    thumb = region.resize((size,size), Image.ANTIALIAS)
    return thumb